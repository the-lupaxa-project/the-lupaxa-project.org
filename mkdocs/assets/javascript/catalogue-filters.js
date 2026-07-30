/**
 * Searchable catalogue filters for projects, organisations, and policies.
 */

(() => {
  "use strict";

  const { onPageRender } = window.LupaxaPageLifecycle;

  const URL_PARAM_SEARCH = "search";
  const URL_PARAM_CATEGORY = "category";
  const URL_PARAM_ORG = "org";
  const FALLBACK_ORG = "Other";
  const CATALOGUE_LOCALE = "en-GB";

  /**
   * Build catalogue selector config from a short id prefix.
   *
   * @param {Object} options
   * @param {string} options.id
   * @param {string} options.singular
   * @param {string} options.plural
   * @param {boolean} [options.organisation=false]
   * @returns {Object}
   */
  function catalogueConfig({
    id,
    singular,
    plural,
    organisation = false,
  }) {
    const config = {
      singular,
      plural,
      filtersSelector: `[data-${id}-filters]`,
      catalogueSelector: `[data-${id}-catalogue]`,
      searchSelector: `[data-${id}-search]`,
      categorySelector: `[data-${id}-category]`,
      clearSelector: `[data-${id}-clear]`,
      summarySelector: `[data-${id}-summary]`,
      emptySelector: `[data-${id}-empty]`,
    };

    if (organisation) {
      config.organisationSelector = `[data-${id}-organisation]`;
    }

    return config;
  }

  /**
   * Convert text into a consistent comparison value.
   *
   * @param {string} value
   * @returns {string}
   */
  function normaliseCatalogueValue(value) {
    return String(value ?? "")
      .toLocaleLowerCase(CATALOGUE_LOCALE)
      .replace(/\s+/g, " ")
      .trim();
  }

  /**
   * Add alphabetically sorted options to a select element.
   *
   * @param {HTMLSelectElement} select
   * @param {Map<string, string>} options
   */
  function addCatalogueOptions(select, options) {
    Array.from(options.entries())
      .sort((left, right) =>
        left[1].localeCompare(right[1], CATALOGUE_LOCALE),
      )
      .forEach(([value, label]) => {
        const option = document.createElement("option");

        option.value = value;
        option.textContent = label;

        select.append(option);
      });
  }

  /**
   * Return the categories attached to a catalogue card.
   *
   * @param {HTMLElement} card
   * @returns {{ values: string[], labels: string[] }}
   */
  function getCatalogueCategories(card) {
    const labels = Array.from(
      card.querySelectorAll(".catalogue-category"),
    )
      .map((category) => category.textContent?.trim() || "")
      .filter(Boolean);

    return {
      labels,
      values: labels.map(normaliseCatalogueValue),
    };
  }

  /**
   * Turn an organisation logo into a link to the Projects catalogue.
   *
   * The organisation is passed through the "org" URL parameter so that the
   * Projects page opens with the matching organisation filter selected.
   *
   * @param {HTMLImageElement} logo
   * @param {string} organisation
   * @param {string} projectsPath
   */
  function addOrganisationProjectLink(
    logo,
    organisation,
    projectsPath,
  ) {
    if (
      !logo ||
      !organisation ||
      logo.closest("[data-organisation-project-link]")
    ) {
      return;
    }

    const url = new URL(projectsPath, window.location.href);

    url.searchParams.set(URL_PARAM_ORG, organisation);

    const link = document.createElement("a");

    link.href = url.href;
    link.dataset.organisationProjectLink = "";
    link.setAttribute(
      "aria-label",
      `View projects from ${organisation}`,
    );

    logo.replaceWith(link);
    link.append(logo);
  }

  /**
   * Remove catalogue filter parameters from the current URL.
   */
  function clearCatalogueUrlParameters() {
    const url = new URL(window.location.href);

    url.searchParams.delete(URL_PARAM_SEARCH);
    url.searchParams.delete(URL_PARAM_CATEGORY);
    url.searchParams.delete(URL_PARAM_ORG);

    window.history.replaceState(
      window.history.state,
      "",
      `${url.pathname}${url.search}${url.hash}`,
    );
  }

  /**
   * Remove temporary options created for URL-supplied filter values.
   *
   * @param {HTMLSelectElement} select
   */
  function removeUrlFilterOptions(select) {
    select
      .querySelectorAll("option[data-url-filter-option]")
      .forEach((option) => {
        option.remove();
      });
  }

  /**
   * Initialise one searchable catalogue.
   *
   * @param {Object} config
   */
  function initialiseCatalogue(config) {
    const filterPanel = document.querySelector(
      config.filtersSelector,
    );
    const catalogue = document.querySelector(
      config.catalogueSelector,
    );

    if (
      !filterPanel ||
      !catalogue ||
      filterPanel.dataset.initialised === "true"
    ) {
      return;
    }

    const searchInput = filterPanel.querySelector(
      config.searchSelector,
    );
    const categorySelect = filterPanel.querySelector(
      config.categorySelector,
    );
    const clearButton = filterPanel.querySelector(
      config.clearSelector,
    );
    const summary = filterPanel.querySelector(
      config.summarySelector,
    );
    const emptyState = document.querySelector(
      config.emptySelector,
    );

    const organisationSelect = config.organisationSelector
      ? filterPanel.querySelector(config.organisationSelector)
      : null;

    if (
      !searchInput ||
      !categorySelect ||
      !clearButton ||
      !summary ||
      (config.organisationSelector && !organisationSelect)
    ) {
      return;
    }

    filterPanel.dataset.initialised = "true";

    const cards = Array.from(
      catalogue.querySelectorAll(":scope > ul > li"),
    );

    const categoryOptions = new Map();
    const organisationOptions = new Map();

    const cardData = cards.map((card) => {
      const categories = getCatalogueCategories(card);
      const logo = card.querySelector(".catalogue-logo");

      const organisationLabel =
        logo?.dataset.organisation?.trim() || "";

      const organisationValue = normaliseCatalogueValue(
        organisationLabel,
      );

      categories.labels.forEach((label, index) => {
        categoryOptions.set(categories.values[index], label);
      });

      if (organisationSelect) {
        const optionLabel = organisationLabel || FALLBACK_ORG;
        const optionValue =
          normaliseCatalogueValue(optionLabel);

        organisationOptions.set(optionValue, optionLabel);
      }

      return {
        element: card,
        categories: categories.values,
        organisation: organisationSelect
          ? organisationValue ||
            normaliseCatalogueValue(FALLBACK_ORG)
          : "",
        searchableText: normaliseCatalogueValue(
          [
            card.textContent || "",
            organisationLabel,
            ...categories.labels,
          ].join(" "),
        ),
      };
    });

    addCatalogueOptions(categorySelect, categoryOptions);

    if (organisationSelect) {
      addCatalogueOptions(
        organisationSelect,
        organisationOptions,
      );
    }

    /**
     * Select a URL-supplied filter value.
     *
     * When the value does not exist among the generated options, add a
     * temporary option so that the requested filter remains active and the
     * catalogue correctly displays its empty state.
     *
     * @param {HTMLSelectElement} select
     * @param {string} value
     */
    const applySelectFilter = (select, value) => {
      const normalisedValue =
        normaliseCatalogueValue(value);

      const optionExists = Array.from(select.options).some(
        (option) => option.value === normalisedValue,
      );

      if (!optionExists) {
        const option = document.createElement("option");

        option.value = normalisedValue;
        option.textContent = value.trim();
        option.dataset.urlFilterOption = "";

        select.append(option);
      }

      select.value = normalisedValue;
    };

    /**
     * Populate available controls from the current URL.
     */
    const applyInitialFilters = () => {
      const urlParameters = new URLSearchParams(
        window.location.search,
      );

      const search = urlParameters.get(URL_PARAM_SEARCH);
      const category = urlParameters.get(URL_PARAM_CATEGORY);
      const organisation = urlParameters.get(URL_PARAM_ORG);

      if (search !== null) {
        searchInput.value = search;
      }

      if (category !== null) {
        applySelectFilter(categorySelect, category);
      }

      if (organisation !== null && organisationSelect) {
        applySelectFilter(organisationSelect, organisation);
      }
    };

    /**
     * Read the current filter control values.
     *
     * @returns {{
     *   searchTerm: string,
     *   selectedCategory: string,
     *   selectedOrganisation: string
     * }}
     */
    const readActiveFilters = () => ({
      searchTerm: normaliseCatalogueValue(searchInput.value),
      selectedCategory: normaliseCatalogueValue(
        categorySelect.value,
      ),
      selectedOrganisation: organisationSelect
        ? normaliseCatalogueValue(organisationSelect.value)
        : "",
    });

    /**
     * Apply visibility to each card for the active filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedCategory: string,
     *   selectedOrganisation: string
     * }} filters
     * @returns {number}
     */
    const applyCardVisibility = (filters) => {
      let visibleCount = 0;

      cardData.forEach((card) => {
        const matchesSearch =
          filters.searchTerm === "" ||
          card.searchableText.includes(filters.searchTerm);

        const matchesCategory =
          filters.selectedCategory === "" ||
          card.categories.includes(filters.selectedCategory);

        const matchesOrganisation =
          filters.selectedOrganisation === "" ||
          card.organisation === filters.selectedOrganisation;

        const isVisible =
          matchesSearch &&
          matchesCategory &&
          matchesOrganisation;

        card.element.hidden = !isVisible;

        if (isVisible) {
          visibleCount += 1;
        }
      });

      return visibleCount;
    };

    /**
     * Update the summary label for the current result set.
     *
     * @param {number} visibleCount
     */
    const updateSummary = (visibleCount) => {
      const totalCount = cardData.length;

      const itemLabel =
        totalCount === 1 ? config.singular : config.plural;

      if (visibleCount === totalCount) {
        summary.textContent =
          `Showing all ${totalCount} ${itemLabel}`;
      } else {
        summary.textContent =
          `Showing ${visibleCount} of ${totalCount} ` +
          `${itemLabel}`;
      }
    };

    /**
     * Enable or disable the clear button from the active filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedCategory: string,
     *   selectedOrganisation: string
     * }} filters
     */
    const updateClearButton = (filters) => {
      clearButton.disabled =
        filters.searchTerm === "" &&
        filters.selectedCategory === "" &&
        filters.selectedOrganisation === "";
    };

    /**
     * Show or hide the empty-state element.
     *
     * @param {number} visibleCount
     */
    const updateEmptyState = (visibleCount) => {
      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
    };

    /**
     * Keep the URL synchronised with the current filters.
     *
     * @param {{
     *   searchTerm: string,
     *   selectedCategory: string,
     *   selectedOrganisation: string
     * }} filters
     */
    const syncUrlWithFilters = (filters) => {
      const params = new URLSearchParams();

      if (filters.searchTerm) {
        params.set(URL_PARAM_SEARCH, searchInput.value.trim());
      }

      if (filters.selectedCategory) {
        params.set(URL_PARAM_CATEGORY, categorySelect.value);
      }

      if (filters.selectedOrganisation) {
        params.set(URL_PARAM_ORG, organisationSelect.value);
      }

      const url = new URL(window.location.href);

      url.search = params.toString();

      window.history.replaceState(
        window.history.state,
        "",
        `${url.pathname}${url.search}${url.hash}`,
      );
    };

    /**
     * Apply all active catalogue filters.
     */
    const updateCatalogue = () => {
      const filters = readActiveFilters();
      const visibleCount = applyCardVisibility(filters);

      updateSummary(visibleCount);
      updateClearButton(filters);
      updateEmptyState(visibleCount);
      syncUrlWithFilters(filters);
    };

    /**
     * Reset all controls and remove filter parameters from the URL.
     */
    const clearFilters = () => {
      searchInput.value = "";
      categorySelect.value = "";
      removeUrlFilterOptions(categorySelect);

      if (organisationSelect) {
        organisationSelect.value = "";
        removeUrlFilterOptions(organisationSelect);
      }

      clearCatalogueUrlParameters();
      updateCatalogue();
      searchInput.focus();
    };

    searchInput.addEventListener("input", updateCatalogue);
    categorySelect.addEventListener("change", updateCatalogue);
    clearButton.addEventListener("click", clearFilters);

    if (organisationSelect) {
      organisationSelect.addEventListener(
        "change",
        updateCatalogue,
      );
    }

    /**
     * Category pills set the category filter on this page.
     */
    catalogue
      .querySelectorAll(".catalogue-category")
      .forEach((pill) => {
        if (pill.dataset.categoryFilterBound === "true") {
          return;
        }

        pill.dataset.categoryFilterBound = "true";
        pill.setAttribute(
          "aria-label",
          `Filter by ${pill.textContent?.trim() || "category"}`,
        );

        pill.addEventListener("click", (event) => {
          event.preventDefault();
          event.stopPropagation();

          const label = pill.textContent?.trim() || "";

          if (!label) {
            return;
          }

          applySelectFilter(categorySelect, label);
          updateCatalogue();
          categorySelect.focus({ preventScroll: true });
        });
      });

    /**
     * Organisation logos set the organisation filter on this page.
     */
    if (organisationSelect) {
      catalogue
        .querySelectorAll("img.catalogue-logo[data-organisation]")
        .forEach((logo) => {
          if (logo.dataset.organisationFilterBound === "true") {
            return;
          }

          const organisation =
            logo.dataset.organisation?.trim() || "";

          if (!organisation) {
            return;
          }

          logo.dataset.organisationFilterBound = "true";

          let control = logo.closest(
            "[data-organisation-filter-control]",
          );

          if (!control) {
            control = document.createElement("button");
            control.type = "button";
            control.dataset.organisationFilterControl = "";
            logo.replaceWith(control);
            control.append(logo);
          }

          control.setAttribute(
            "aria-label",
            `Filter by ${organisation}`,
          );

          control.addEventListener("click", (event) => {
            event.preventDefault();
            event.stopPropagation();

            applySelectFilter(organisationSelect, organisation);
            updateCatalogue();
            organisationSelect.focus({ preventScroll: true });
          });
        });
    }

    applyInitialFilters();
    updateCatalogue();
  }

  const catalogueConfigurations = [
    catalogueConfig({
      id: "project",
      singular: "project",
      plural: "projects",
      organisation: true,
    }),
    catalogueConfig({
      id: "organisation",
      singular: "organisation",
      plural: "organisations",
    }),
    catalogueConfig({
      id: "policy",
      singular: "policy",
      plural: "policies",
    }),
    catalogueConfig({
      id: "article",
      singular: "article",
      plural: "articles",
    }),
  ];

  /**
   * Resolve the Projects catalogue path from the current page location.
   *
   * @returns {string}
   */
  function projectsCataloguePath() {
    const path = window.location.pathname;

    if (path.includes("/organisations")) {
      return "../projects/";
    }

    if (path.includes("/projects")) {
      return "./";
    }

    return "projects/";
  }

  /**
   * Wrap organisation logos in links to the Projects catalogue (org filter).
   *
   * Skipped on the Projects page itself — logos filter in-place there.
   */
  function linkOrganisationLogos() {
    const path = window.location.pathname;

    if (path.includes("/projects")) {
      return;
    }

    const projectsPath = projectsCataloguePath();

    document
      .querySelectorAll("img.catalogue-logo[data-organisation]")
      .forEach((logo) => {
        const organisation = logo.dataset.organisation?.trim() || "";

        addOrganisationProjectLink(logo, organisation, projectsPath);
      });
  }

  /**
   * On pages without a filter panel (e.g. featured projects on home), category
   * pills navigate to the Projects catalogue with that category selected.
   */
  function linkStandaloneCategoryPills() {
    const path = window.location.pathname;

    if (
      path.includes("/organisations") ||
      path.includes("/projects") ||
      path.includes("/policies") ||
      path.includes("/articles")
    ) {
      return;
    }

    document.querySelectorAll(".catalogue-category").forEach((pill) => {
      if (pill.dataset.categoryFilterBound === "true") {
        return;
      }

      const label = pill.textContent?.trim() || "";

      if (!label) {
        return;
      }

      pill.dataset.categoryFilterBound = "true";
      pill.setAttribute("aria-label", `View projects in ${label}`);

      pill.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();

        const url = new URL("projects/", window.location.href);

        url.searchParams.set(URL_PARAM_CATEGORY, label);
        window.location.href = url.href;
      });
    });
  }

  /**
   * Initialise every catalogue present on the current page.
   */
  function initialiseCatalogues() {
    linkOrganisationLogos();
    catalogueConfigurations.forEach(initialiseCatalogue);
    linkStandaloneCategoryPills();
  }

  onPageRender(initialiseCatalogues);
})();
