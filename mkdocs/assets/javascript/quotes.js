/**
 * Quotes masonry wall — thin page wrapper around LupaxaMasonryWall.
 */
(() => {
  "use strict";

  const initQuotesWall = () => {
    const wall = window.LupaxaMasonryWall;
    if (!wall) return;

    wall.init({
      wallId: "quotes-wall",
      masonrySelector: ".quotes-masonry",
      filterSelector: ".quotes-filter",
      cardSelector: ".quote-card",
    });
  };

  const lifecycle = window.LupaxaPageLifecycle;
  if (lifecycle && lifecycle.onPageRender) {
    lifecycle.onPageRender(initQuotesWall);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initQuotesWall);
  } else {
    initQuotesWall();
  }
})();
