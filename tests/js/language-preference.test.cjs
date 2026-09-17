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
