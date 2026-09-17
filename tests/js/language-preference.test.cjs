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
});
