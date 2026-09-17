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

  const translatorAvailable = (api) =>
    Boolean(api && typeof api.create === "function");

  const shouldShowFallback = (locale, available, dismissed) =>
    locale !== "en" && !available && !dismissed;

  const applyDocumentLang = (doc, locale) => {
    if (doc && doc.documentElement) {
      doc.documentElement.lang = locale;
    }
  };

  let translatedNodes = new WeakSet();
  let activeLocale = "en";
  let translatorCache = { locale: null, translator: null, api: null };

  const resetTranslatedNodes = () => {
    translatedNodes = new WeakSet();
  };

  const rememberLocale = (locale) => {
    if (activeLocale !== locale) {
      resetTranslatedNodes();
      activeLocale = locale;
    }
  };

  const destroyTranslator = (translator) => {
    if (translator && typeof translator.destroy === "function") {
      try {
        translator.destroy();
      } catch (_error) {
        /* ignore */
      }
    }
  };

  const clearTranslatorCache = () => {
    destroyTranslator(translatorCache.translator);
    translatorCache = { locale: null, translator: null, api: null };
  };

  const splitEdgeWhitespace = (value) => {
    const text = String(value ?? "");
    const trimmed = text.trim();
    if (!trimmed) {
      return { lead: "", trimmed: "", trail: "" };
    }
    const start = text.indexOf(trimmed);
    return {
      lead: text.slice(0, start),
      trimmed,
      trail: text.slice(start + trimmed.length),
    };
  };

  const translateTextNodes = async (nodes, translator, isCurrent) => {
    for (const node of nodes) {
      if (!isCurrent()) {
        return;
      }
      if (translatedNodes.has(node)) {
        continue;
      }
      const original = node.nodeValue;
      const { lead, trimmed, trail } = splitEdgeWhitespace(original);
      if (!trimmed) {
        continue;
      }
      try {
        const next = await translator.translate(trimmed);
        if (!isCurrent()) {
          return;
        }
        if (typeof next === "string" && next.length > 0) {
          node.nodeValue = lead + next + trail;
          translatedNodes.add(node);
        }
      } catch (_error) {
        node.nodeValue = original;
      }
    }
  };

  const runTranslation = async ({
    locale,
    api,
    roots,
    document: doc,
    generation,
    currentGeneration,
  }) => {
    rememberLocale(locale);
    if (locale === "en") {
      clearTranslatorCache();
      applyDocumentLang(doc, "en");
      return { status: "skipped", generation };
    }
    const isCurrent = () => currentGeneration() === generation;
    if (!translatorAvailable(api)) {
      return { status: "fallback", generation };
    }
    let translator = null;
    if (
      translatorCache.locale === locale &&
      translatorCache.api === api &&
      translatorCache.translator
    ) {
      translator = translatorCache.translator;
    } else {
      try {
        translator = await api.create({
          sourceLanguage: "en",
          targetLanguage: locale,
        });
      } catch (_error) {
        return { status: "failed", generation };
      }
      if (!isCurrent()) {
        destroyTranslator(translator);
        return { status: "skipped", generation };
      }
      clearTranslatorCache();
      translatorCache = { locale, translator, api };
    }
    if (!isCurrent()) {
      return { status: "skipped", generation };
    }
    const nodes = [];
    for (const root of roots || []) {
      nodes.push(...collectTextNodes(root));
    }
    await translateTextNodes(nodes, translator, isCurrent);
    if (!isCurrent()) {
      return { status: "skipped", generation };
    }
    applyDocumentLang(doc, locale);
    return { status: "ok", generation };
  };

  let generation = 0;

  const browserTranslatorApi = () => {
    if (typeof self !== "undefined" && self.Translator) {
      return self.Translator;
    }
    return null;
  };

  const onPickerChange = async (value, { storage, reload, apply }) => {
    const locale = writePreference(storage, value);
    if (locale === "en") {
      reload();
      return locale;
    }
    await apply(locale);
    return locale;
  };

  const attach = (deps) => {
    const doc = deps.document;
    const storage = safeStorage(deps.storage);
    const session = safeStorage(deps.sessionStorage);
    const reload = deps.reload;
    const api =
      deps.translatorApi !== undefined
        ? deps.translatorApi
        : browserTranslatorApi();
    const picker = doc.getElementById("lupaxa-lang");
    const note = doc.getElementById("lupaxa-lang-fallback");
    const dismiss = doc.getElementById("lupaxa-lang-fallback-dismiss");

    const setNoteHidden = (hidden) => {
      if (note) {
        note.hidden = hidden;
      }
    };

    const dismissed = () =>
      session.getItem(FALLBACK_DISMISS_KEY) === "1";

    const apply = async (locale) => {
      generation += 1;
      const myGeneration = generation;
      const roots = [];
      const header = doc.querySelector(".md-header");
      const main = doc.querySelector(".md-main");
      const footer = doc.querySelector(".md-footer");
      if (header) {
        roots.push(header);
      }
      if (main) {
        roots.push(main);
      }
      if (footer) {
        roots.push(footer);
      }
      const result = await runTranslation({
        locale,
        api,
        roots,
        document: doc,
        generation: myGeneration,
        currentGeneration: () => generation,
      });
      if (result.status === "fallback" || result.status === "failed") {
        if (result.status === "failed" && typeof console !== "undefined") {
          console.warn("Lupaxa language preference: translation failed");
        }
        setNoteHidden(!shouldShowFallback(locale, false, dismissed()));
      } else {
        setNoteHidden(true);
      }
      if (picker) {
        picker.value = locale;
      }
      return result;
    };

    if (picker && !picker.dataset.lupaxaLangBound) {
      picker.dataset.lupaxaLangBound = "1";
      picker.addEventListener("change", () => {
        onPickerChange(picker.value, {
          storage,
          reload,
          apply,
        });
      });
    }
    if (dismiss && !dismiss.dataset.lupaxaLangBound) {
      dismiss.dataset.lupaxaLangBound = "1";
      dismiss.addEventListener("click", () => {
        session.setItem(FALLBACK_DISMISS_KEY, "1");
        setNoteHidden(true);
      });
    }

    const locale = readPreference(storage);
    if (picker) {
      picker.value = locale;
    }
    return apply(locale);
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
    translatorAvailable,
    shouldShowFallback,
    applyDocumentLang,
    translateTextNodes,
    runTranslation,
    onPickerChange,
    attach,
  };
})();

if (typeof window !== "undefined") {
  window.LupaxaLanguagePreference = LupaxaLanguagePreference;
}

if (
  typeof window !== "undefined" &&
  window.document &&
  window.LupaxaPageLifecycle &&
  typeof window.LupaxaPageLifecycle.onPageRender === "function"
) {
  window.LupaxaPageLifecycle.onPageRender(() => {
    LupaxaLanguagePreference.attach({
      document: window.document,
      storage: window.localStorage,
      sessionStorage: window.sessionStorage,
      reload: () => window.location.reload(),
    });
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = LupaxaLanguagePreference;
}
