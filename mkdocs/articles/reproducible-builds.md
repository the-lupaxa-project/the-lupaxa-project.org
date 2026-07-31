---
title: Reproducible Builds
published: true
publish_date: "2026-04-09"
hide:
- navigation
- toc
description: Lightweight reproducible builds for small tools. Pinning inputs, killing
  nondeterminism, and getting to bit-for-bit or near-identical releases without
  enterprise ceremony.
tags:
- Security
- Engineering
---

# Reproducible Builds: Same Inputs, Same Artefacts

A reproducible build means that given the same source and toolchain inputs, you get the same artefact bytes, or close enough that you can explain the differences. For small open-source tools this is less about academic purity and more about trust. Someone else can rebuild what you shipped and check that it matches.

## 1. Why It Matters

Reproducibility helps:

- Users verify releases match source
- Maintainers debug "works in CI only" packaging bugs
- Supply-chain stories that go beyond "trust this binary"

It pairs with signing: signatures say who published; reproducibility says what was built.

## 2. Pin the Inputs

- Lock dependencies
- Record language/runtime version
- Pin OS packages in container builds
- Note architecture (`amd64`/`arm64`)

Floating toolchains produce floating artefacts.

## 3. Kill Obvious Nondeterminism

Common culprits:

- Embedded timestamps
- Random temporary paths in archives
- Unsorted dict/hash iteration in packagers
- Local usernames in file metadata

Prefer `SOURCE_DATE_EPOCH` and stable archive settings when your ecosystem supports them.

## 4. Practical, Not Perfect

Bit-for-bit identity is ideal. **Practical reproducibility** (same functional content, documented toolchain) is still valuable when absolute identity is hard (some proprietary linkers, some language ecosystems).

Say what you guarantee. Honesty beats fake hermetic claims.

## 5. Automate a Rebuild Check

In CI:

1. Build the artefact
2. Build again in a clean environment (or compare against a known builder)
3. Diff digests

Fail the job when digests diverge unexpectedly.

## 6. Publish Enough for Others to Retry

Release notes or a `BUILD.md` should list:

- Exact commands
- Toolchain versions
- Expected artefact names and hashes

If only your laptop can reproduce, it is not reproducible.

## 7. Closing Thoughts

Reproducible builds shrink the trust gap between source and binary. Pin inputs, remove noise, check digests in CI, and document how a stranger can rebuild. That is enough ceremony to matter and not enough to stop shipping.
