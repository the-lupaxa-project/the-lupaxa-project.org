/**
 * Rewrite article prev/next links to follow a filtered catalogue sequence.
 *
 * When the articles catalogue has active filters, catalogue-filters.js stores
 * the visible cards in sessionStorage. This script applies that sequence on
 * article pages in the same tab. Direct visits / cleared filters keep the
 * build-time A–Z pager from the template.
 */

(() => {
  "use strict";

  const { onPageRender } = window.LupaxaPageLifecycle;

  const ARTICLE_PAGER_STORAGE_KEY = "lupaxa.articlePager";

  /**
   * Current article slug from the page path.
   *
   * @returns {string}
   */
  function currentArticleSlug() {
    const path = window.location.pathname
      .replace(/\/index\.html$/i, "")
      .replace(/\/+$/, "");
    const match = path.match(/\/articles\/([^/]+)$/i);

    return match ? match[1] : "";
  }

  /**
   * Fill or clear a prev/next slot.
   *
   * @param {HTMLElement | null} slot
   * @param {{ title: string, url: string } | null} item
   * @param {string} label
   */
  function updatePagerSlot(slot, item, label) {
    if (!slot) {
      return;
    }

    slot.replaceChildren();

    if (!item) {
      return;
    }

    const link = document.createElement("a");
    link.className = "lupaxa-article-pager__link";
    link.href = item.url;

    const labelEl = document.createElement("span");
    labelEl.className = "lupaxa-article-pager__label";
    labelEl.textContent = label;

    const titleEl = document.createElement("span");
    titleEl.className = "lupaxa-article-pager__title";
    titleEl.textContent = item.title;

    link.append(labelEl, titleEl);
    slot.append(link);
  }

  /**
   * Apply a stored filtered sequence to the article pager, if present.
   */
  function applyFilteredArticlePager() {
    const pager = document.querySelector(".lupaxa-article-pager");

    if (!pager) {
      return;
    }

    // Reset in case Instant Navigation reused a previously hidden pager.
    pager.hidden = false;

    let payload;

    try {
      const raw = sessionStorage.getItem(ARTICLE_PAGER_STORAGE_KEY);

      if (!raw) {
        return;
      }

      payload = JSON.parse(raw);
    } catch {
      return;
    }

    const sequence = Array.isArray(payload?.sequence)
      ? payload.sequence
      : null;

    if (!sequence || sequence.length === 0) {
      return;
    }

    const currentSlug = currentArticleSlug();

    if (!currentSlug) {
      return;
    }

    const index = sequence.findIndex(
      (item) => item.slug === currentSlug,
    );

    // Article is outside the stored filter set — keep server pager.
    if (index < 0) {
      return;
    }

    const prev = index > 0 ? sequence[index - 1] : null;
    const next =
      index < sequence.length - 1 ? sequence[index + 1] : null;

    if (!prev && !next) {
      pager.hidden = true;
      return;
    }

    updatePagerSlot(
      pager.querySelector(".lupaxa-article-pager__prev"),
      prev,
      "Previous article",
    );
    updatePagerSlot(
      pager.querySelector(".lupaxa-article-pager__next"),
      next,
      "Next article",
    );
  }

  onPageRender(applyFilteredArticlePager);
})();
