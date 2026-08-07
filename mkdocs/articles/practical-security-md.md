---
title: Practical SECURITY.md
published: true
publish_date: "2026-07-31T17:42:00"
hide:
- navigation
- toc
description: A practical SECURITY.md playbook for small projects. What to include,
  example structure, scope statements, and making the security policy easy to find
  and follow.
tags:
- Security
- Open Source
---

# Practical SECURITY.md

You already know disclosures need a door. This article is about the **document behind the door**: a `SECURITY.md` that reporters can follow and maintainers can honour. Short, concrete, and honest beats a copied enterprise policy.

## Put It Where Tools Expect

- Repository root: `SECURITY.md`
- Optional: `.github/SECURITY.md` on GitHub (still keep root or link clearly)
- Link from the README under Support or Security

If people cannot find it in ten seconds, it does not exist.

## A Structure That Works

Keep sections scannable:

1. **Supported versions:** what you still patch
2. **Reporting:** private channel and what to include
3. **Scope:** in and out
4. **Response expectations:** human timelines, not fake SLAs
5. **Safe harbour:** good-faith research welcome
6. **Preferences:** credit, encryption keys if any

One screen on mobile is a good length target for small projects.

## Be Explicit About Scope

In scope examples:

- Vulnerabilities in the latest release line
- Secrets handling bugs in the CLI
- Auth bypass in a shipped server mode

Out of scope examples:

- Issues only in unmodified upstream dependencies (point to upstream)
- Social engineering of maintainers
- Denial of service requiring unrealistic resources
- Bugs in unmaintained major versions

Clarity saves everyone time.

## Tell Reporters What to Send

Ask for:

- Version / commit
- Reproduction steps
- Impact
- Environment notes

Say thank you for concise reports. Do not demand a full consulting engagement.

## Promise Only Your Real Capacity

Example language:

> We aim to acknowledge within a few business days. Fixes land as soon as we can ship a safe release. Critical issues jump the feature queue.

Update the file when capacity changes. An outdated promise is worse than a modest one.

## Keep It Alive

Review `SECURITY.md` when you:

- Cut an old major
- Change reporting channels
- Add a network service mode
- Hand off maintainership

A stale policy is how reports go to abandoned email addresses.

## Closing Thoughts

A useful `SECURITY.md` is a map: where to report, what counts, what to expect. Write it for a tired researcher at midnight, and for future you who has to answer them.
