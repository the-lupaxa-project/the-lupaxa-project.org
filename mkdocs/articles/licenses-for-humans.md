---
title: Licenses for Humans
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: A plain-language guide to open-source licenses for people publishing tools.
  MIT, Apache-2.0, and the GPL family, what each one asks of your users, and how to
  choose without a law degree.
tags:
- Open Source
- Community
---

# Licenses for Humans: Choosing How Others Can Use Your Code

Publishing code without a license does not mean "do whatever you want." In many places it means the opposite: all rights reserved by default. A clear `LICENSE` file is how you tell people what they may do, and what you expect in return.

This is not legal advice. It is a practical map for tool authors who want to make a deliberate choice.

## 1. Why a License Matters

A license answers:

- Can others use this commercially?
- Must they share modifications?
- Must they preserve copyright notices?
- Are patent grants included?
- What happens to liability?

Without answers, careful organisations will not touch your project. Careless ones may use it anyway and create confusion later.

## 2. Permissive Licenses: MIT and BSD-style

**MIT** and similar BSD licenses are short and popular for libraries and tools.

Typical spirit:

- Use, copy, modify, distribute, sell
- Keep the copyright and license notice
- Software provided "as is"

They maximise adoption. They do not require downstream projects to open their modifications.

## 3. Apache License 2.0

**Apache-2.0** is also permissive, with clearer patent language and an explicit contribution license grant. Many companies prefer it for that clarity.

If you care about patent peace and still want wide reuse, Apache-2.0 is a common choice.

## 4. Copyleft: GPL and Friends

**GPL** family licenses require that derivative works distributed to others remain under compatible copyleft terms. That protects user freedom to study and modify software, and it can complicate proprietary embedding.

Choose copyleft when sharing-alike is a core value of the project. Do not end up there by accident because a dependency forced your hand. Understand the tree you are building on.

**LGPL** is often used for libraries when you want copyleft on the library itself but allow linking from differently licensed applications. Details matter; read before you commit.

## 5. How to Choose Without Spiralling

A simple heuristic for many Lupaxa-style tools:

- **Want maximum reuse and simplicity?** MIT or BSD
- **Want permissive + patent clarity?** Apache-2.0
- **Want strong share-alike?** GPL (and accept the ecosystem effects)

Also check:

- Licenses of your dependencies (they constrain you)
- Whether your community already standardises on one license
- Whether you need a contributor agreement (often you do not for small projects)

## 6. Put It Where Humans Look

- Add a `LICENSE` file at the repository root
- Mention the license in the README
- Use the correct SPDX identifier in package metadata when applicable

Ambiguous "see license" links to nowhere help nobody.

## 7. Closing Thoughts

A license is part of your product's honesty. Pick one on purpose, publish it clearly, and stay consistent across the repository. That small act turns source code into something others can safely build on.
