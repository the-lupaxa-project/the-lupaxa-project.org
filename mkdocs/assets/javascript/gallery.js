/**
 * Gallery masonry and media viewer.
 * Re-inits on Material instant navigation via LupaxaPageLifecycle.
 */
(() => {
  "use strict";

  const GAP = 16;
  let resizeBound = false;
  let resizeTimer = null;
  let activeMasonry = null;
  let activeLightbox = null;
  let keydownBound = false;

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

  const matchesFilter = (card, selected) => {
    if (selected === "all") return true;
    if (selected === "photos") return card.getAttribute("data-media") === "image";
    if (selected === "videos") return card.getAttribute("data-media") === "video";
    return cardTags(card).includes(selected);
  };

  const columnCountForWidth = (width) => {
    const cols = Math.floor((width + GAP) / (280 + GAP));
    return Math.max(1, Math.min(cols, 6));
  };

  const layoutMasonry = (masonry) => {
    const cards = Array.from(masonry.querySelectorAll(".photo-card"));
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

  const renderMasonry = (masonry, cards, selected) => {
    cards.forEach((card) => {
      card.style.transform = "";
      card.style.position = "";
      card.style.width = "";
      card.remove();
    });
    cards
      .filter((card) => matchesFilter(card, selected))
      .forEach((card) => masonry.appendChild(card));
    layoutMasonry(masonry);
  };

  const focusableIn = (root) =>
    Array.from(
      root.querySelectorAll(
        'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
      )
    ).filter((element) => !element.hasAttribute("disabled") && element.offsetParent !== null);

  const initLightbox = (masonry, wall) => {
    const lightbox = document.getElementById("gallery-lightbox");
    if (!lightbox) return { open() {}, handleKeydown() {}, destroy() {} };

    const image = lightbox.querySelector(".lightbox-image");
    const video = lightbox.querySelector(".lightbox-video");
    const commentEl = lightbox.querySelector(".lightbox-comment");
    const dateEl = lightbox.querySelector(".lightbox-date");
    const closeBtn = lightbox.querySelector(".lightbox-close");
    const backdrop = lightbox.querySelector(".lightbox-backdrop");
    const prevBtn = lightbox.querySelector(".lightbox-prev");
    const nextBtn = lightbox.querySelector(".lightbox-next");
    let lastFocus = null;
    let currentIndex = -1;

    const visibleOpenButtons = () =>
      Array.from(masonry.querySelectorAll(".photo-card .photo-open"));

    const stopVideo = () => {
      video.pause();
      video.removeAttribute("src");
      video.removeAttribute("poster");
      video.load();
      video.hidden = true;
    };

    const clearImage = () => {
      image.removeAttribute("src");
      image.alt = "";
      image.hidden = true;
    };

    const showFromButton = (button) => {
      const src = button.getAttribute("data-src") || "";
      const type = button.getAttribute("data-type") || "image";
      const poster = button.getAttribute("data-poster") || "";
      const comment = button.getAttribute("data-comment") || "";
      const date = button.getAttribute("data-date") || "";

      stopVideo();
      clearImage();

      if (type === "video") {
        video.src = src;
        if (poster) video.poster = poster;
        video.hidden = false;
        video.currentTime = 0;
        const playPromise = video.play();
        if (playPromise && typeof playPromise.catch === "function") {
          playPromise.catch(() => {});
        }
      } else {
        image.src = src;
        image.alt = comment;
        image.hidden = false;
      }

      commentEl.textContent = comment;
      commentEl.hidden = !comment;
      dateEl.textContent = date;
      dateEl.hidden = !date;
    };

    const reset = () => {
      lightbox.hidden = true;
      document.body.classList.remove("lightbox-open");
      if (wall) wall.inert = false;
      stopVideo();
      clearImage();
      currentIndex = -1;
    };

    const close = () => {
      if (lightbox.hidden) return;
      reset();
      if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
      lastFocus = null;
    };

    const destroy = () => {
      reset();
      lastFocus = null;
    };

    const open = (button) => {
      const buttons = visibleOpenButtons();
      currentIndex = buttons.indexOf(button);
      if (currentIndex < 0) currentIndex = 0;
      lastFocus = button;
      showFromButton(button);
      lightbox.hidden = false;
      document.body.classList.add("lightbox-open");
      if (wall) wall.inert = true;
      closeBtn.focus();
    };

    const step = (delta) => {
      const buttons = visibleOpenButtons();
      if (!buttons.length) return;
      currentIndex = (currentIndex + delta + buttons.length) % buttons.length;
      const button = buttons[currentIndex];
      lastFocus = button;
      showFromButton(button);
    };

    const handleKeydown = (event) => {
      if (lightbox.hidden) return;

      if (event.key === "Escape") {
        event.preventDefault();
        close();
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        step(1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        step(-1);
      } else if (event.key === "Tab") {
        const focusables = focusableIn(lightbox);
        if (!focusables.length) {
          event.preventDefault();
          return;
        }
        const first = focusables[0];
        const last = focusables[focusables.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    };

    closeBtn.addEventListener("click", close);
    backdrop.addEventListener("click", close);
    prevBtn.addEventListener("click", () => step(-1));
    nextBtn.addEventListener("click", () => step(1));

    return { open, handleKeydown, destroy };
  };

  const cleanupActiveLightbox = () => {
    if (activeLightbox) activeLightbox.destroy();
    activeLightbox = null;
  };

  const initGalleryWall = () => {
    cleanupActiveLightbox();
    const masonry = document.querySelector(".gallery-masonry");
    const filters = document.querySelectorAll(".gallery-filter");
    const wall = document.getElementById("gallery-wall");
    if (!masonry || !filters.length) {
      activeMasonry = null;
      return;
    }

    activeMasonry = masonry;
    activeLightbox = initLightbox(masonry, wall);
    const nodes = masonry.querySelectorAll(".photo-card");
    const cards =
      wall && wall.getAttribute("data-shuffle") === "true"
        ? shuffle(nodes)
        : Array.from(nodes);
    let selected = "all";

    renderMasonry(masonry, cards, selected);

    filters.forEach((button) => {
      button.addEventListener("click", () => {
        selected = button.getAttribute("data-filter");
        filters.forEach((filter) =>
          filter.classList.toggle("is-active", filter === button)
        );
        renderMasonry(masonry, cards, selected);
      });
    });

    masonry.addEventListener("click", (event) => {
      const openButton = event.target.closest(".photo-open");
      if (!openButton || !masonry.contains(openButton)) return;
      activeLightbox.open(openButton);
    });

    masonry.querySelectorAll(".photo-image").forEach((media) => {
      const relayout = () => layoutMasonry(masonry);
      if (media.tagName === "VIDEO") {
        media.addEventListener("loadedmetadata", relayout);
        media.addEventListener("error", relayout);
      } else if (!media.complete) {
        media.addEventListener("load", relayout);
        media.addEventListener("error", relayout);
      }
    });

    if (!resizeBound) {
      resizeBound = true;
      window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          if (activeMasonry && document.contains(activeMasonry)) {
            layoutMasonry(activeMasonry);
          }
        }, 100);
      });
    }

    if (!keydownBound) {
      keydownBound = true;
      document.addEventListener("keydown", (event) => {
        if (activeLightbox) activeLightbox.handleKeydown(event);
      });
    }
  };

  const lifecycle = window.LupaxaPageLifecycle;
  if (lifecycle) {
    lifecycle.onDocumentReady(initGalleryWall);
    lifecycle.onInstantNavigation(initGalleryWall);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGalleryWall);
  } else {
    initGalleryWall();
  }
})();
