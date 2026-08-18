/**
 * Catalogue pages index many cards as sections of one document.
 * Material then hides lower-scoring matches behind "and N more".
 * Open those groups so every matching card is visible.
 */

(() => {
  "use strict";

  const { onPageRender } = window.LupaxaPageLifecycle;

  /**
   * Reveal every collapsed same-page search match.
   *
   * @param {ParentNode} root
   */
  const revealGroupedMatches = (root) => {
    root
      .querySelectorAll("details.md-search-result__more")
      .forEach((details) => {
        details.open = true;
      });
  };

  const bindSearchResults = () => {
    const list = document.querySelector(".md-search-result__list");

    if (!list || list.dataset.lupaxaSearchBound === "true") {
      return;
    }

    list.dataset.lupaxaSearchBound = "true";
    revealGroupedMatches(list);

    const observer = new MutationObserver(() => {
      revealGroupedMatches(list);
    });

    observer.observe(list, { childList: true, subtree: true });
  };

  onPageRender(bindSearchResults);
})();
