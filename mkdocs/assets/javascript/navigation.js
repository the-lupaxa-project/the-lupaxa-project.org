/**
 * Keep the custom header navigation active state synchronised with
 * MkDocs Material instant navigation.
 */

(() => {
  "use strict";

  const normalisePath = (value) => {
    const url = new URL(value, window.location.origin);

    const path = url.pathname
      .replace(/\/index\.html$/, "/")
      .replace(/\/+$/, "");

    return path || "/";
  };

  const updateActiveNavigation = () => {
    const currentPath = normalisePath(window.location.href);

    document
      .querySelectorAll(".lupaxa-header__nav-item")
      .forEach((item) => {
        const link = item.querySelector(
          ".lupaxa-header__nav-link",
        );

        if (!link) {
          return;
        }

        const linkPath = normalisePath(link.href);

        const isActive =
          linkPath === "/"
            ? currentPath === "/"
            : currentPath === linkPath ||
              currentPath.startsWith(`${linkPath}/`);

        item.classList.toggle(
          "lupaxa-header__nav-item--active",
          isActive,
        );

        if (isActive) {
          link.setAttribute("aria-current", "page");
        } else {
          link.removeAttribute("aria-current");
        }
      });
  };

  const scheduleUpdate = () => {
    requestAnimationFrame(updateActiveNavigation);
  };

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      updateActiveNavigation,
      { once: true },
    );
  } else {
    updateActiveNavigation();
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(scheduleUpdate);
  }

  window.addEventListener("popstate", scheduleUpdate);
})();

/**
 * Convert text into a consistent comparison value.
 *
 * @param {string} value
 * @returns {string}
 */
function normaliseCatalogueValue(value) {
  return String(value ?? "")
    .toLocaleLowerCase("en-GB")
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
      left[1].localeCompare(right[1], "en-GB"),
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

  url.searchParams.set("org", organisation);

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

  url.searchParams.delete("search");
  url.searchParams.delete("category");
  url.searchParams.delete("org");

  window.history.replaceState(
    window.history.state,
    "",
    `${url.pathname}${url.search}${url.hash}`,
  );
}

/**
 * Initialise one searchable catalogue.
 *
 * Supported filters:
 * - free-text search;
 * - category selection;
 * - optional organisation selection;
 * - initial filter values supplied through URL parameters;
 * - optional organisation-logo links to the Projects catalogue.
 *
 * @param {Object} config
 * @param {string} config.name
 * @param {string} config.singular
 * @param {string} config.plural
 * @param {string} config.filtersSelector
 * @param {string} config.catalogueSelector
 * @param {string} config.searchSelector
 * @param {string} config.categorySelector
 * @param {string} config.clearSelector
 * @param {string} config.summarySelector
 * @param {string} config.emptySelector
 * @param {string} [config.organisationSelector]
 * @param {string} [config.projectsPath]
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
      const optionLabel = organisationLabel || "Other";
      const optionValue = normaliseCatalogueValue(optionLabel);

      organisationOptions.set(optionValue, optionLabel);
    }

    if (
      config.projectsPath &&
      logo &&
      organisationLabel
    ) {
      addOrganisationProjectLink(
        logo,
        organisationLabel,
        config.projectsPath,
      );
    }

    return {
      element: card,
      categories: categories.values,
      organisation: organisationSelect
        ? organisationValue ||
          normaliseCatalogueValue("Other")
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

    const search = urlParameters.get("search");
    const category = urlParameters.get("category");
    const organisation = urlParameters.get("org");

    if (search !== null) {
      searchInput.value = search;
    }

    if (category !== null) {
      applySelectFilter(
        categorySelect,
        category,
      );
    }

    if (
      organisation !== null &&
      organisationSelect
    ) {
      applySelectFilter(
        organisationSelect,
        organisation,
      );
    }
  };

  /**
   * Apply all active catalogue filters.
   */
  const updateCatalogue = () => {
    const searchTerm = normaliseCatalogueValue(
      searchInput.value,
    );

    const selectedCategory = normaliseCatalogueValue(
      categorySelect.value,
    );

    const selectedOrganisation = organisationSelect
      ? normaliseCatalogueValue(
          organisationSelect.value,
        )
      : "";

    let visibleCount = 0;

    cardData.forEach((card) => {
      const matchesSearch =
        searchTerm === "" ||
        card.searchableText.includes(searchTerm);

      const matchesCategory =
        selectedCategory === "" ||
        card.categories.includes(selectedCategory);

      const matchesOrganisation =
        selectedOrganisation === "" ||
        card.organisation === selectedOrganisation;

      const isVisible =
        matchesSearch &&
        matchesCategory &&
        matchesOrganisation;

      card.element.hidden = !isVisible;

      if (isVisible) {
        visibleCount += 1;
      }
    });

    const totalCount = cardData.length;

    const itemLabel =
      totalCount === 1
        ? config.singular
        : config.plural;

    if (visibleCount === totalCount) {
      summary.textContent =
        `Showing all ${totalCount} ${itemLabel}`;
    } else {
      summary.textContent =
        `Showing ${visibleCount} of ${totalCount} ` +
        `${itemLabel}`;
    }

    clearButton.disabled =
      searchTerm === "" &&
      selectedCategory === "" &&
      selectedOrganisation === "";

    if (emptyState) {
      emptyState.hidden = visibleCount !== 0;
    }
    // Keep the URL synchronised with the current filters.

    const params = new URLSearchParams();

    if (searchTerm) {
      params.set("search", searchInput.value.trim());
    }

    if (selectedCategory) {
      params.set("category", categorySelect.value);
    }

    if (selectedOrganisation) {
      params.set("org", organisationSelect.value);
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
   * Reset all controls and remove filter parameters from the URL.
   */
  const clearFilters = () => {
    searchInput.value = "";
    categorySelect.value = "";

    if (organisationSelect) {
      organisationSelect.value = "";
    }

    clearCatalogueUrlParameters();
    updateCatalogue();
    searchInput.focus();
  };

  searchInput.addEventListener(
    "input",
    updateCatalogue,
  );

  categorySelect.addEventListener(
    "change",
    updateCatalogue,
  );

  clearButton.addEventListener(
    "click",
    clearFilters,
  );

  if (organisationSelect) {
    organisationSelect.addEventListener(
      "change",
      updateCatalogue,
    );
  }

  applyInitialFilters();
  updateCatalogue();
}

/**
 * Catalogue configurations.
 */
const catalogueConfigurations = [
  {
    name: "projects",
    singular: "project",
    plural: "projects",
    filtersSelector: "[data-project-filters]",
    catalogueSelector: "[data-project-catalogue]",
    searchSelector: "[data-project-search]",
    organisationSelector:
      "[data-project-organisation]",
    categorySelector: "[data-project-category]",
    clearSelector: "[data-project-clear]",
    summarySelector: "[data-project-summary]",
    emptySelector: "[data-project-empty]",
  },
  {
    name: "organisations",
    singular: "organisation",
    plural: "organisations",
    filtersSelector: "[data-organisation-filters]",
    catalogueSelector:
      "[data-organisation-catalogue]",
    searchSelector: "[data-organisation-search]",
    categorySelector:
      "[data-organisation-category]",
    clearSelector: "[data-organisation-clear]",
    summarySelector:
      "[data-organisation-summary]",
    emptySelector: "[data-organisation-empty]",

    /*
     * This path is resolved relative to the Organisations page.
     *
     * For example:
     * /organisations/ -> /projects/
     */
    projectsPath: "../projects/",
  },
  {
    name: "policies",
    singular: "policy",
    plural: "policies",
    filtersSelector: "[data-policy-filters]",
    catalogueSelector: "[data-policy-catalogue]",
    searchSelector: "[data-policy-search]",
    categorySelector: "[data-policy-category]",
    clearSelector: "[data-policy-clear]",
    summarySelector: "[data-policy-summary]",
    emptySelector: "[data-policy-empty]",
  },
];

/**
 * Initialise every catalogue present on the current page.
 */
function initialiseCatalogues() {
  catalogueConfigurations.forEach(initialiseCatalogue);
}

/*
 * Support both normal page loads and MkDocs Material instant navigation.
 */

if (document.readyState === "loading") {
  document.addEventListener(
    "DOMContentLoaded",
    initialiseCatalogues,
    { once: true },
  );
} else {
  initialiseCatalogues();
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    requestAnimationFrame(initialiseCatalogues);
  });
}
