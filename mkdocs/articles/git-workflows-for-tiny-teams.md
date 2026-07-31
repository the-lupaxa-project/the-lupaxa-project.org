---
title: Git Workflows for Tiny Teams
published: true
hide:
- navigation
- toc
description: Practical Git workflows for small teams and solo maintainers. Trunk-based
  development, short-lived branches, pull requests, and release tags without enterprise
  branching theatre.
tags:
- Engineering
- Process
---

# Git Workflows for Tiny Teams: Enough Process, Not Too Much

Git workflows expand to fill the org chart. Tiny teams do not need seven long-lived branches and a release train committee. They need a habit that keeps `main` releasable and history understandable.

## 1. Prefer a Releasable Mainline

Keep `main` (or `trunk`) green. Merge only what you would be willing to ship. Feature flags and small PRs help; giant week-long branches fight you.

If `main` is routinely broken, you do not have a workflow problem. You have a testing and ownership problem.

## 2. Short-Lived Branches

Branch for a change, open a PR, merge, delete. Days, not months. Long-lived feature branches are where conflicts and abandoned work breed.

Solo maintainers can still use PRs against themselves. The review diff and CI are the point.

## 3. Pull Requests as Conversation

A PR should explain *why*. Link the issue. Keep the diff reviewable. Squash or rebase according to the project's norm, but pick one and document it.

"LGTM" on a 2,000-line tangle is not review; it is hope.

## 4. Protect the Default Branch

Require CI to pass before merge when you can. Restrict force-push on `main`. That single protection prevents a surprising class of disasters.

## 5. Tags for Releases

Release from tags, not from "whatever was on my laptop." Annotated tags plus CI publish jobs keep history and artefacts aligned. See release automation for the pipeline shape.

## 6. Skip Enterprise Branch Zoo (Until You Need It)

`develop`, `release/*`, `hotfix/*`, and environment branches earn their keep at scale. For two people shipping a CLI, they mostly add merge debt.

Add structure when pain appears, like parallel releases or long support windows, not because a blog post diagram looked official.

## 7. Closing Thoughts

A tiny-team Git workflow is a releasable mainline, short branches, protected merges, and tags for ships. Everything else should justify the complexity it adds, or leave.
