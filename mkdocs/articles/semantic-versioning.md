---
title: Semantic Versioning
published: true
publish_date: "2026-06-11"
hide:
- navigation
- toc
description: Semantic versioning as it actually plays out in open-source tools. What
  counts as breaking, how to live in 0.x honestly, why changelogs are part of the version
  number, and how to keep upgrades boring.
tags:
- Open Source
- Engineering
---

# Semantic Versioning in the Real World

Semantic Versioning (SemVer) looks simple: `MAJOR.MINOR.PATCH`. In practice, maintainers argue about what counts as breaking, users pin ranges that surprise them, and `0.x` becomes a permanent lifestyle. Used well, SemVer is a contract. Used poorly, it is decoration.

This article focuses on how SemVer behaves for real libraries and CLIs.

## 1. The Contract in Plain Language

For a public API after `1.0.0`:

- **MAJOR** for incompatible API changes
- **MINOR** for backwards-compatible functionality
- **PATCH** for backwards-compatible bug fixes

The key phrase is *public API*. Private helpers, undocumented behaviour, and accidental quirks are not automatically part of the contract. But if you documented them by example and people now rely on them, you have shipped a de facto API anyway.

## 2. What "Breaking" Usually Means

Breaking changes include:

- Removing or renaming public functions, flags, or config keys
- Changing default behaviour users depend on
- Tightening validation in ways that reject previously accepted input
- Changing output formats that scripts parse

Not automatically breaking:

- Refactors with the same behaviour
- Performance improvements that preserve results
- Adding optional parameters with safe defaults
- Fixing undefined behaviour you never promised

When unsure, ask: "Would a careful user have to change their code or scripts?" If yes, bump major, or deprecate first.

## 3. Life Before 1.0.0

In `0.x`, SemVer allows sharper edges: anything may change. That freedom is useful while the design is still moving. It is also a trust test.

Be explicit in the README:

- Whether `0.x` is experimental or merely pre-1.0 polish
- How aggressive you are about breaking changes
- What you consider stable even in `0.x`

Users pin `0.x` ranges differently than `1.x`. Do not pretend a chaotic `0.x` is production-solid without saying so.

## 4. Deprecate Before You Destroy

A kind breaking change is announced early:

1. Document the new approach
2. Emit warnings when the old path is used (when practical)
3. Give time in minor releases
4. Remove in a major release with a changelog note

Silent removals train users to fear upgrades.

## 5. Changelogs Are Part of Versioning

A version number without a changelog is a rumour.

For each release, say:

- What changed
- What broke
- How to migrate
- Whether action is required

"Bug fixes and improvements" is not a changelog. It is a shrug.

## 6. Ranges, Lockfiles, and Reality

Consumers should:

- Use lockfiles for applications
- Prefer cautious ranges for libraries
- Read majors before upgrading blindly

Publishers should:

- Avoid surprise majors for trivial renames
- Not hide breaks in minors "because it is easier"
- Tag releases consistently in git and packages

## 7. Closing Thoughts

SemVer is communication. The number tells users how scared they should be to upgrade. Make that signal boringly reliable and your project becomes easy to depend on, which is one of the highest compliments in open source.
