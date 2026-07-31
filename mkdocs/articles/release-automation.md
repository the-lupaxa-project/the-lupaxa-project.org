---
title: Release Automation
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: How to make releases boring. Tags as the source of truth, changelogs people
  can read, scoped publishing tokens, and CI guardrails that stop a bad release before
  it reaches a registry.
tags:
- CI/CD
- Open Source
---

# Release Automation: Shipping Without Heroics

A release should be a boring button, or better, a tag that triggers a known pipeline. When shipping depends on a maintainer remembering twelve manual steps, releases become rare, late, and error-prone.

Here is a practical shape for small open-source projects.

## 1. Decide What a Release Is

Define the artefacts you publish:

- Git tag and GitHub Release
- Package registry artefact (PyPI, npm, crates…)
- Documentation for that version
- Optional binaries or container images

Write the checklist once. Then make machines execute it.

## 2. Tags as the Source of Truth

A clean pattern:

1. Merge to the release branch / main
2. Ensure CI is green
3. Create an annotated tag (`v1.4.2`)
4. Let CI build, test, and publish from the tag

Avoid publishing from dirty local trees. If it is not in git, it is not a release.

## 3. Changelogs That Humans Read

Automate collection where you can (conventional commits, PR labels), but keep a human pass for majors.

Every release note should answer:

- What is new?
- What broke?
- What must users do?

Link issues/PRs when helpful. Skip empty marketing fluff.

## 4. GitHub Releases and Packages

GitHub Releases are a friendly landing page for notes and binaries. Attach checksums for anything you distribute. Publish packages with tokens scoped as tightly as practical, stored as secrets, never in the repository.

## 5. Guardrails in CI

Before publish jobs run:

- Tests must pass
- Lint/type checks you rely on must pass
- Build reproducibility checks if you ship binaries
- Abort if the version already exists on the registry

A publish job that can run twice safely (idempotent) saves panic later.

## 6. Separate Build From Deploy Privileges

Use environments and protected secrets so routine PRs cannot publish. Tag builds can request publishing credentials; pull requests should not.

## 7. Practice Dry Runs

Provide a dry-run mode for packaging and note generation. Rehearse the release pipeline on a pre-release tag when the project is young. Confidence comes from repetition, not optimism.

## 8. Closing Thoughts

Release automation turns "we should ship" into "we shipped." Combine tags, green CI, honest changelogs, and constrained secrets. Maintainers get their weekends back, and users get predictable upgrades.
