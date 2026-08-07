---
title: Security Disclosures That Work
published: true
publish_date: "2026-07-30T16:03:17"
hide:
- navigation
- toc
description: Practical security disclosure for small open-source projects. SECURITY.md,
  private reporting, triage, credit, and promises maintainers can actually keep.
tags:
- Security
- Open Source
---

# Security Disclosures That Work: Reporting Bugs Without the Chaos

Every project that ships code will eventually hear about a vulnerability, or wish it had. A workable disclosure process is not a corporate programme. It is a clear door for good-faith reporters and a calm path for maintainers who still have day jobs.

This article is for small open-source tools and libraries that want to do the right thing without promising a 24/7 SOC.

## Put the Door Where People Look

Add a `SECURITY.md` at the repository root. GitHub and many scanners look for it.

It should answer:

- How do I report a security issue privately?
- What is in scope?
- What should I include?
- What can I expect for response timing?

Link it from the README. A buried wiki page is not a disclosure channel.

## Prefer Private Channels First

Public issues are fine for ordinary bugs. Security findings that enable exploitation should stay private until a fix or mitigation is ready.

Common options:

- GitHub private vulnerability reporting
- A dedicated security email
- A form that does not publish submissions

Pick one primary channel and say so clearly. Two half-documented paths create missed reports.

## Promise Only What You Can Keep

Do not invent SLA theatre. Honest language beats fake urgency:

- "We aim to acknowledge within a few days"
- "Fixes land when we can ship a safe release"
- "Critical issues get priority over feature work"

Reporters respect clarity. They distrust corporate countdown clocks that maintainers cannot honour.

## Ask for Useful Details

Invite reporters to include:

- Affected versions
- Steps to reproduce
- Impact (what an attacker gains)
- Suggested fix, if they have one

Thank people who send a minimal PoC. Do not demand unpaid consulting disguised as a bug report.

## Triage Like an Engineer

When a report arrives:

1. Confirm it is real and in scope
2. Estimate impact and exploitability
3. Decide patch, mitigate, or decline with reasons
4. Coordinate disclosure timing if the issue is serious

Out-of-scope reports deserve a short polite reply, not silence.

## Fix, Release, Then Talk

Ship the fix (or mitigation) before broad public write-ups when practical. Credit reporters who want credit. Document the issue in release notes without teaching attackers more than they need.

If you cannot patch immediately, document temporary mitigations for users.

## Closing Thoughts

A good disclosure process is hospitality for people trying to help you. Make the door obvious, keep reports private until users are safer, and promise only what a small team can deliver. That is enough to be a responsible maintainer.
