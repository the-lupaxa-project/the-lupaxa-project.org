/**
 * Viewer language preference: store a locale and translate the current
 * English page in the browser. No locale URLs.
 */
"use strict";

const LupaxaLanguagePreference = (() => {
  const STORAGE_KEY = "lupaxa-lang";
  const FALLBACK_DISMISS_KEY = "lupaxa-lang-fallback-dismissed";
  const LOCALES = ["en", "fr", "de"];
  const SKIP_TAGS = new Set(["PRE", "CODE", "SCRIPT", "STYLE", "NOSCRIPT"]);

  const safeStorage = (backing) => {
    if (!backing) {
      return memoryBacking();
    }
    try {
      const probe = "__lupaxa_lang_probe__";
      backing.setItem(probe, "1");
      backing.removeItem(probe);
      return backing;
    } catch (_error) {
      return memoryBacking();
    }
  };

  const memoryBacking = () => {
    const map = new Map();
    return {
      getItem(key) {
        return map.has(key) ? map.get(key) : null;
      },
      setItem(key, value) {
        map.set(key, String(value));
      },
      removeItem(key) {
        map.delete(key);
      },
    };
  };

  const normaliseLocale = (value) =>
    LOCALES.includes(value) ? value : "en";

  const readPreference = (storage) => {
    let raw = null;
    try {
      raw = storage.getItem(STORAGE_KEY);
    } catch (_error) {
      return "en";
    }
    if (raw === null || raw === undefined || raw === "") {
      return "en";
    }
    const locale = normaliseLocale(raw);
    if (locale !== raw) {
      try {
        storage.setItem(STORAGE_KEY, locale);
      } catch (_error) {
        /* ignore */
      }
    }
    return locale;
  };

  const writePreference = (storage, value) => {
    const locale = normaliseLocale(value);
    try {
      storage.setItem(STORAGE_KEY, locale);
    } catch (_error) {
      /* ignore */
    }
    return locale;
  };

  const isUrlLikeText = (value) => {
    const text = String(value || "").trim();
    return /^(https?:\/\/|www\.)/i.test(text);
  };

  const isSkippableElement = (el) => {
    if (!el || el.nodeType !== 1) {
      return false;
    }
    if (SKIP_TAGS.has(el.tagName)) {
      return true;
    }
    if (el.getAttribute && el.getAttribute("translate") === "no") {
      return true;
    }
    if (el.classList && el.classList.contains("notranslate")) {
      return true;
    }
    return false;
  };

  const shouldSkipNode = (node) => {
    if (!node) {
      return true;
    }
    if (node.nodeType === 3 && isUrlLikeText(node.nodeValue)) {
      return true;
    }
    let el = node.nodeType === 3 ? node.parentElement : node;
    while (el) {
      if (isSkippableElement(el)) {
        return true;
      }
      el = el.parentElement;
    }
    return false;
  };

  const collectTextNodes = (root) => {
    const found = [];
    const visit = (node) => {
      if (!node) {
        return;
      }
      if (node.nodeType === 3) {
        if (String(node.nodeValue || "").trim() && !shouldSkipNode(node)) {
          found.push(node);
        }
        return;
      }
      if (node.nodeType === 1 && isSkippableElement(node)) {
        return;
      }
      const kids = node.childNodes || [];
      for (let i = 0; i < kids.length; i += 1) {
        visit(kids[i]);
      }
    };
    visit(root);
    return found;
  };

  return {
    STORAGE_KEY,
    FALLBACK_DISMISS_KEY,
    LOCALES,
    safeStorage,
    readPreference,
    writePreference,
    isUrlLikeText,
    isSkippableElement,
    shouldSkipNode,
    collectTextNodes,
  };
})();

if (typeof window !== "undefined") {
  window.LupaxaLanguagePreference = LupaxaLanguagePreference;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = LupaxaLanguagePreference;
}
