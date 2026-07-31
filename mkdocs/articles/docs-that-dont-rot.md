---
title: Docs That Don't Rot
published: true
hide:
- navigation
- toc
description: How to keep project documentation alive. Examples as tests, docs sites
  that ship with releases, screenshots that stay honest, and habits that stop docs
  from quietly lying.
tags:
- Documentation
- Open Source
---

# Docs That Don't Rot: Keeping Instructions True

Documentation starts accurate and dies of neglect. A single wrong flag in an example can cost newcomers an afternoon, and cost you an issue you will answer forever. Docs that do not rot are less about writing more and more about wiring docs into the same feedback loops as code.

## 1. Treat Examples as Code

If an example is important, automate it.

Approaches that work:

- Run README snippets in CI
- Generate CLI help from the real parser
- Store fixtures next to the docs that use them
- Prefer copy-pasteable blocks over paraphrases

When docs and code disagree, CI should fail before users do.

## 2. Prefer Generated Truth

Human prose goes stale. Generated surfaces stay closer to reality:

- `--help` output
- API references from docstrings/type hints
- Config tables from schemas

Write narrative around generated truth. Do not hand-maintain a second shadow API.

## 3. Screenshots Are Liabilities

Screenshots age faster than text.

If you need them:

- Capture only stable UI
- Store sources and recreate with a script when possible
- Date or version-stamp sensitive images
- Prefer SVG/diagrams for concepts that do not need pixels

A wrong screenshot is worse than no screenshot.

## 4. Ship Docs With the Version

Docs for `v2` that only exist on `main` confuse everyone.

Practices that help:

- Publish versioned docs for released tags
- Note which version a page applies to
- Keep a short "what's new" for major jumps
- Link the README to the docs for *this* release line

## 5. Delete Dead Pages

Obsolete guides are traps. Archive or delete pages for removed features. A smaller docs set that is true beats a museum of maybe.

## 6. Make Doc Fixes Easy

Lower the cost of correction:

- "Edit this page" links
- Tiny contribution path for typos
- Review doc PRs with the same care as code when behaviour is involved

The person who hits the wrong instruction first is often your best editor.

## 7. Closing Thoughts

Documentation decays unless you attach it to tests, releases, and contribution habits. Write less fiction, generate more truth, and kill pages that no longer earn their place. That is how docs stay trustworthy as the project moves.
