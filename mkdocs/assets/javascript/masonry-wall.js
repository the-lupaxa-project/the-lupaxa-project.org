/**
 * Shared masonry wall primitives for Quotes and Gallery.
 * Page scripts supply selectors and optional filter matching.
 */
(() => {
  "use strict";

  const GAP = 16;
  let resizeBound = false;
  let resizeTimer = null;
  const activeMasonries = new Set();

  const shuffle = (nodes) => {
    const arr = Array.from(nodes);
    for (let i = arr.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  };

  const cardTags = (card) =>
    (card.getAttribute("data-tags") || "").split("|").filter(Boolean);

  const defaultMatchesFilter = (card, selected) =>
    selected === "all" || cardTags(card).includes(selected);

  const columnCountForWidth = (width) => {
    const cols = Math.floor((width + GAP) / (280 + GAP));
    return Math.max(1, Math.min(cols, 6));
  };

  const layoutMasonry = (masonry, cardSelector) => {
    const cards = Array.from(masonry.querySelectorAll(cardSelector));
    const width = masonry.clientWidth;
    const cols = columnCountForWidth(width);
    const colWidth = cols === 1 ? width : (width - GAP * (cols - 1)) / cols;
    const heights = Array.from({ length: cols }, () => 0);

    masonry.classList.add("is-laid-out");
    masonry.style.height = "";

    cards.forEach((card) => {
      card.style.width = `${colWidth}px`;
      card.style.position = "absolute";
      card.style.left = "0";
      card.style.top = "0";
    });

    cards.forEach((card) => {
      let col = 0;
      for (let i = 1; i < cols; i += 1) {
        if (heights[i] < heights[col]) col = i;
      }
      const x = col * (colWidth + GAP);
      const y = heights[col];
      card.style.transform = `translate(${x}px, ${y}px)`;
      heights[col] += card.offsetHeight + GAP;
    });

    const total = heights.length ? Math.max(...heights) : 0;
    masonry.style.height = `${Math.max(0, total - GAP)}px`;
  };

  const renderMasonry = (masonry, cards, selected, matchesFilter, cardSelector) => {
    cards.forEach((card) => {
      card.style.transform = "";
      card.style.position = "";
      card.style.width = "";
      card.remove();
    });
    cards
      .filter((card) => matchesFilter(card, selected))
      .forEach((card) => masonry.appendChild(card));
    layoutMasonry(masonry, cardSelector);
  };

  const bindResize = () => {
    if (resizeBound) return;
    resizeBound = true;
    window.addEventListener("resize", () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => {
        activeMasonries.forEach((entry) => {
          if (document.contains(entry.masonry)) {
            layoutMasonry(entry.masonry, entry.cardSelector);
          } else {
            activeMasonries.delete(entry);
          }
        });
      }, 100);
    });
  };

  /**
   * @param {object} options
   * @param {string} options.wallId
   * @param {string} options.masonrySelector
   * @param {string} options.filterSelector
   * @param {string} options.cardSelector
   * @param {(card: Element, selected: string) => boolean} [options.matchesFilter]
   * @returns {{ masonry: Element, wall: Element | null, layout: () => void } | null}
   */
  const init = (options) => {
    const {
      wallId,
      masonrySelector,
      filterSelector,
      cardSelector,
      matchesFilter = defaultMatchesFilter,
    } = options;

    const masonry = document.querySelector(masonrySelector);
    const filters = document.querySelectorAll(filterSelector);
    if (!masonry || !filters.length) return null;

    const wall = wallId ? document.getElementById(wallId) : null;
    const nodes = masonry.querySelectorAll(cardSelector);
    const cards =
      wall && wall.getAttribute("data-shuffle") === "true"
        ? shuffle(nodes)
        : Array.from(nodes);
    let selected = "all";

    const layout = () => layoutMasonry(masonry, cardSelector);
    const render = (nextSelected) =>
      renderMasonry(masonry, cards, nextSelected, matchesFilter, cardSelector);

    render(selected);

    filters.forEach((button) => {
      button.addEventListener("click", () => {
        selected = button.getAttribute("data-filter");
        filters.forEach((filter) =>
          filter.classList.toggle("is-active", filter === button)
        );
        render(selected);
      });
    });

    activeMasonries.forEach((entry) => {
      if (entry.masonry === masonry || !document.contains(entry.masonry)) {
        activeMasonries.delete(entry);
      }
    });
    activeMasonries.add({ masonry, cardSelector });
    bindResize();

    return { masonry, wall, layout };
  };

  window.LupaxaMasonryWall = {
    init,
    cardTags,
    layoutMasonry,
  };
})();
