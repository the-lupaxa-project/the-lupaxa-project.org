"use strict";

const { describe, it } = require("node:test");
const assert = require("node:assert/strict");
const path = require("node:path");

const lib = require(path.join(
  __dirname,
  "..",
  "..",
  "mkdocs",
  "assets",
  "javascript",
  "language-preference.js",
));

function memoryStorage(initial) {
  const map = new Map(Object.entries(initial || {}));
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
}

function element(tag, attrs, children) {
  const el = {
    nodeType: 1,
    tagName: tag.toUpperCase(),
    attributes: attrs || {},
    childNodes: children || [],
    parentElement: null,
    getAttribute(name) {
      if (!Object.prototype.hasOwnProperty.call(this.attributes, name)) {
        return null;
      }
      return this.attributes[name];
    },
    classList: {
      contains: (name) =>
        String((attrs && attrs.class) || "")
          .split(/\s+/)
          .includes(name),
    },
  };
  for (const child of el.childNodes) {
    child.parentElement = el;
  }
  return el;
}

function text(value) {
  return { nodeType: 3, nodeValue: value, parentElement: null };
}

describe("readPreference", () => {
  it("defaults to en when empty", () => {
    assert.equal(lib.readPreference(memoryStorage()), "en");
  });

  it("returns a stored locale", () => {
    assert.equal(
      lib.readPreference(memoryStorage({ "lupaxa-lang": "fr" })),
      "fr",
    );
  });

  it("rewrites an unknown value to en", () => {
    const storage = memoryStorage({ "lupaxa-lang": "zz" });
    assert.equal(lib.readPreference(storage), "en");
    assert.equal(storage.getItem("lupaxa-lang"), "en");
  });
});

describe("writePreference", () => {
  it("stores fr", () => {
    const storage = memoryStorage();
    assert.equal(lib.writePreference(storage, "fr"), "fr");
    assert.equal(storage.getItem("lupaxa-lang"), "fr");
  });

  it("stores en for an unknown value", () => {
    const storage = memoryStorage();
    assert.equal(lib.writePreference(storage, "zz"), "en");
    assert.equal(storage.getItem("lupaxa-lang"), "en");
  });
});

describe("shouldSkipNode", () => {
  it("skips text inside pre and code", () => {
    const codeText = text("print('hi')");
    const code = element("code", {}, [codeText]);
    const pre = element("pre", {}, [code]);
    assert.equal(lib.shouldSkipNode(codeText), true);
    assert.equal(lib.shouldSkipNode(pre.childNodes[0].childNodes[0] || codeText), true);
  });

  it("skips translate=no and .notranslate ancestors", () => {
    const brand = text("The Lupaxa Project");
    const strong = element("strong", { translate: "no" }, [brand]);
    const skipped = text("Acme");
    const named = element("span", { class: "notranslate" }, [skipped]);
    assert.equal(lib.shouldSkipNode(brand), true);
    assert.equal(lib.shouldSkipNode(skipped), true);
  });

  it("does not skip a normal paragraph", () => {
    const copy = text("Browse projects");
    element("p", {}, [copy]);
    assert.equal(lib.shouldSkipNode(copy), false);
  });
});

describe("collectTextNodes", () => {
  it("returns only translatable text nodes", () => {
    const para = text("Hello");
    const brand = text("The Lupaxa Project");
    const root = element("div", {}, [
      element("p", {}, [para]),
      element("h1", { translate: "no" }, [brand]),
      element("code", {}, [text("id")]),
    ]);
    const nodes = lib.collectTextNodes(root);
    assert.deepEqual(
      nodes.map((node) => node.nodeValue),
      ["Hello"],
    );
  });
});

describe("isUrlLikeText", () => {
  it("detects http(s) and www URLs", () => {
    assert.equal(lib.isUrlLikeText("https://github.com/org/repo"), true);
    assert.equal(lib.isUrlLikeText("View on GitHub"), false);
  });
});

describe("shouldShowFallback", () => {
  it("shows only when a non-en locale has no API and is not dismissed", () => {
    assert.equal(lib.shouldShowFallback("fr", false, false), true);
    assert.equal(lib.shouldShowFallback("fr", true, false), false);
    assert.equal(lib.shouldShowFallback("en", false, false), false);
    assert.equal(lib.shouldShowFallback("de", false, true), false);
  });
});

describe("applyDocumentLang", () => {
  it("sets documentElement.lang", () => {
    const doc = { documentElement: { lang: "en" } };
    lib.applyDocumentLang(doc, "fr");
    assert.equal(doc.documentElement.lang, "fr");
  });
});

describe("translateTextNodes", () => {
  it("rewrites a normal paragraph with the translator", async () => {
    const copy = text("Browse projects");
    element("p", {}, [copy]);
    const translator = {
      async translate(value) {
        return `FR:${value}`;
      },
    };
    await lib.translateTextNodes([copy], translator, () => true);
    assert.equal(copy.nodeValue, "FR:Browse projects");
  });

  it("leaves a node in English when translate throws", async () => {
    const copy = text("Browse projects");
    const translator = {
      async translate() {
        throw new Error("quota");
      },
    };
    await lib.translateTextNodes([copy], translator, () => true);
    assert.equal(copy.nodeValue, "Browse projects");
  });

  it("does not apply a stale generation", async () => {
    const copy = text("Browse projects");
    let allow = true;
    const translator = {
      async translate(value) {
        return `FR:${value}`;
      },
    };
    await lib.translateTextNodes([copy], translator, () => allow && ((allow = false), false));
    assert.equal(copy.nodeValue, "Browse projects");
  });

  it("does not prefix again on a second pass", async () => {
    const copy = text("Hello");
    const translator = {
      async translate(value) {
        return `FR:${value}`;
      },
    };
    await lib.translateTextNodes([copy], translator, () => true);
    await lib.translateTextNodes([copy], translator, () => true);
    assert.equal(copy.nodeValue, "FR:Hello");
  });

  it("preserves leading and trailing whitespace", async () => {
    const copy = text(" Hello ");
    const translator = {
      async translate(value) {
        return `FR:${value}`;
      },
    };
    await lib.translateTextNodes([copy], translator, () => true);
    assert.equal(copy.nodeValue, " FR:Hello ");
  });
});

describe("runTranslation", () => {
  it("skips work for en and leaves lang en", async () => {
    const copy = text("Hello");
    const root = element("p", {}, [copy]);
    const doc = { documentElement: { lang: "en" } };
    const result = await lib.runTranslation({
      locale: "en",
      api: { create: async () => ({ translate: async () => "nope" }) },
      roots: [root],
      document: doc,
      generation: 1,
      currentGeneration: () => 1,
    });
    assert.equal(result.status, "skipped");
    assert.equal(copy.nodeValue, "Hello");
    assert.equal(doc.documentElement.lang, "en");
  });

  it("translates and sets html lang on success", async () => {
    const copy = text("Hello");
    const root = element("p", {}, [copy]);
    const doc = { documentElement: { lang: "en" } };
    const result = await lib.runTranslation({
      locale: "fr",
      api: {
        create: async () => ({
          translate: async (value) => `FR:${value}`,
        }),
      },
      roots: [root],
      document: doc,
      generation: 2,
      currentGeneration: () => 2,
    });
    assert.equal(result.status, "ok");
    assert.equal(copy.nodeValue, "FR:Hello");
    assert.equal(doc.documentElement.lang, "fr");
  });

  it("returns fallback when the API is missing", async () => {
    const copy = text("Hello");
    const root = element("p", {}, [copy]);
    const doc = { documentElement: { lang: "en" } };
    const result = await lib.runTranslation({
      locale: "de",
      api: null,
      roots: [root],
      document: doc,
      generation: 3,
      currentGeneration: () => 3,
    });
    assert.equal(result.status, "fallback");
    assert.equal(copy.nodeValue, "Hello");
    assert.equal(doc.documentElement.lang, "en");
  });

  it("returns failed when create throws and does not loop", async () => {
    const copy = text("Hello");
    const root = element("p", {}, [copy]);
    const doc = { documentElement: { lang: "en" } };
    let creates = 0;
    const result = await lib.runTranslation({
      locale: "fr",
      api: {
        create: async () => {
          creates += 1;
          throw new Error("blocked");
        },
      },
      roots: [root],
      document: doc,
      generation: 4,
      currentGeneration: () => 4,
    });
    assert.equal(result.status, "failed");
    assert.equal(creates, 1);
    assert.equal(copy.nodeValue, "Hello");
    assert.equal(doc.documentElement.lang, "en");
  });

  it("does not prefix again when run twice on the same nodes", async () => {
    const copy = text("Hello");
    const root = element("p", {}, [copy]);
    const doc = { documentElement: { lang: "en" } };
    let creates = 0;
    const api = {
      create: async () => {
        creates += 1;
        return {
          translate: async (value) => `FR:${value}`,
        };
      },
    };
    const base = {
      locale: "fr",
      api,
      roots: [root],
      document: doc,
    };
    await lib.runTranslation({
      ...base,
      generation: 10,
      currentGeneration: () => 10,
    });
    await lib.runTranslation({
      ...base,
      generation: 11,
      currentGeneration: () => 11,
    });
    assert.equal(copy.nodeValue, "FR:Hello");
    assert.equal(doc.documentElement.lang, "fr");
    assert.equal(creates, 1);
  });
});

describe("onPickerChange", () => {
  it("writes fr and does not reload", async () => {
    const storage = memoryStorage();
    let reloads = 0;
    const apply = async () => "ok";
    await lib.onPickerChange("fr", {
      storage,
      reload: () => {
        reloads += 1;
      },
      apply,
    });
    assert.equal(storage.getItem("lupaxa-lang"), "fr");
    assert.equal(reloads, 0);
  });

  it("applies fr when the picker selects fr", async () => {
    const storage = memoryStorage();
    let applied = null;
    await lib.onPickerChange("fr", {
      storage,
      reload: () => {
        throw new Error("should not reload");
      },
      apply: async (locale) => {
        applied = locale;
      },
    });
    assert.equal(applied, "fr");
  });

  it("writes en and reloads", async () => {
    const storage = memoryStorage({ "lupaxa-lang": "fr" });
    let reloads = 0;
    await lib.onPickerChange("en", {
      storage,
      reload: () => {
        reloads += 1;
      },
      apply: async () => {
        throw new Error("should not apply");
      },
    });
    assert.equal(storage.getItem("lupaxa-lang"), "en");
    assert.equal(reloads, 1);
  });
});

function fakeDocument() {
  const changeListeners = [];
  const clickListeners = [];
  const picker = {
    id: "lupaxa-lang",
    value: "en",
    dataset: {},
    addEventListener(type, fn) {
      if (type === "change") {
        changeListeners.push(fn);
      }
    },
  };
  const note = {
    id: "lupaxa-lang-fallback",
    hidden: true,
  };
  const dismiss = {
    id: "lupaxa-lang-fallback-dismiss",
    dataset: {},
    addEventListener(type, fn) {
      if (type === "click") {
        clickListeners.push(fn);
      }
    },
  };
  const ids = {
    "lupaxa-lang": picker,
    "lupaxa-lang-fallback": note,
    "lupaxa-lang-fallback-dismiss": dismiss,
  };
  return {
    documentElement: { lang: "en" },
    getElementById(id) {
      return Object.prototype.hasOwnProperty.call(ids, id) ? ids[id] : null;
    },
    querySelector() {
      return null;
    },
    picker,
    note,
    dismiss,
    changeListeners,
    clickListeners,
  };
}

describe("attach", () => {
  it("shows the fallback note for fr when the API is null", async () => {
    const doc = fakeDocument();
    const storage = memoryStorage({ "lupaxa-lang": "fr" });
    const session = memoryStorage();
    await lib.attach({
      document: doc,
      storage,
      sessionStorage: session,
      reload: () => {},
      translatorApi: null,
    });
    assert.equal(doc.note.hidden, false);
    assert.equal(doc.changeListeners.length, 1);

    doc.clickListeners[0]();
    assert.equal(doc.note.hidden, true);
    assert.equal(session.getItem(lib.FALLBACK_DISMISS_KEY), "1");

    await lib.attach({
      document: doc,
      storage,
      sessionStorage: session,
      reload: () => {},
      translatorApi: null,
    });
    assert.equal(doc.changeListeners.length, 1);
    assert.equal(doc.note.hidden, true);
  });
});
