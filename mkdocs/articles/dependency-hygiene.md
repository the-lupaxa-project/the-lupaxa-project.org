---
title: Dependency Hygiene
published: true
hide:
- navigation
- toc
description: Practical dependency hygiene for small teams and open-source projects.
  Pinning, lockfiles, audits, supply-chain basics, and keeping your supply line
  trustworthy without enterprise ceremony.
tags:
- Security
- Engineering
---

# Dependency Hygiene: Keeping Your Supply Line Honest

Modern software is mostly other people's code glued together with a little of your own. That is powerful and risky. Dependency hygiene is the habit of knowing what you depend on, why you depend on it, and how you will notice when it goes wrong.

This is not about paranoia. It is about not shipping surprises.

## 1. Prefer Fewer, Clearer Dependencies

Every dependency is a trust relationship and a maintenance surface.

Before adding one, ask:

- Can the standard library do this well enough?
- Is this package actively maintained?
- How wide is its own dependency tree?
- Am I pulling a framework to solve a one-function problem?

Small tools especially benefit from restraint. A CLI that installs half the internet to print a certificate has already failed its UX.

## 2. Pin What You Ship

Applications and deployable tools should use lockfiles. They turn "works on my machine" into "works with these exact versions."

Libraries are different: they declare compatible ranges so apps can resolve a single tree. Even then, your CI should test against locked sets so you know what you actually verified.

## 3. Audit Without Theatre

Run vulnerability audits regularly, in CI, not only after an incident.

Then triage like an engineer:

- **Reachability matters.** A CVE in an unused optional extra is not the same as one on your request path.
- **Severity scores are hints**, not commandments.
- **`--force` is not a strategy.** Ignoring findings without notes is how debt becomes breach.

Document accepted risks briefly when you must defer a fix.

## 4. Supply-Chain Basics That Pay Off

Practical controls for small projects:

- Prefer official package registries and HTTPS
- Verify signatures or checksums when the ecosystem supports them
- Avoid copy-pasting install scripts from random blogs into root shells
- Watch for typosquat names when adding packages quickly
- Review sudden maintainer changes on critical dependencies

You do not need a corporate security programme to avoid the obvious traps.

## 5. Keep Updates Boring

Out-of-date dependencies become emergency updates. Emergency updates become outages.

Habits that help:

- Scheduled small upgrades
- Automated pull requests with tests attached
- Reading changelogs for majors before merging
- Removing unused dependencies instead of forever upgrading them

## 6. Own Your Tree

Know how to generate a dependency graph or bill of materials for your project. When someone asks "are we affected by X?", you want an answer in minutes, not an archaeological dig.

## 7. Closing Thoughts

Dependency hygiene is craftsmanship: take only what you need, pin what you release, watch what you trust, and update before fear forces your hand. That is how small open-source tools stay dependable as the ecosystem moves under them.
