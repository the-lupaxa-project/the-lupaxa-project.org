---
title: Responsible Dependency Updates
published: true
hide:
- navigation
- toc
description: A practical cadence for dependency updates — Dependabot-style PRs, ignore
  rules, reading majors, and keeping upgrades boring without ignoring security fixes.
tags:
- Security
- Engineering
---

# Responsible Dependency Updates: Cadence Without Chaos

Dependency hygiene says know your tree. Responsible updates say keep it moving — without merging every noisy PR blind or freezing until the next CVE fire drill.

## 1. Schedule Small, Frequent Upgrades

Weekly or biweekly batched updates beat quarterly monster jumps. Small diffs are reviewable. Large jumps hide breakages and encourage "skip until broken."

Automate PR creation; do not automate merge without tests.

## 2. Let Tests Be the Gate

Update PRs should run the same CI as human PRs. Red CI means fix or roll back — not force-merge because the bot is lonely.

If you lack tests, dependency automation will punish you. That is feedback.

## 3. Triage Security Separately

Critical/high vulns in reachable code get fast-tracked. Low noise in unused optional extras can wait. Reachability and exploitability still matter — see dependency hygiene.

Have a human glance at security PRs even when automation is trusted for patches.

## 4. Use Ignore Rules Sparingly

Ignoring a noisy major forever is how you wake up on an abandoned branch of the ecosystem. Prefer:

- Temporary ignores with expiry
- Grouping related packages
- Documented reasons in the ignore config

## 5. Read Changelogs on Majors

Minors and patches can be skimmed when CI is strong. Majors need eyes: breaking changes, licence shifts, new network defaults, telemetry.

SemVer is a contract; changelogs are the negotiation.

## 6. Own Transitive Pain

Sometimes the fix is upgrading a parent, replacing a package, or vendoring less. "Waiting for upstream" is fine for days, not for seasons, when the CVE is exploitable in your context.

## 7. Closing Thoughts

Responsible updates are a rhythm: automate proposals, gate on tests, fast-track real risk, and read majors. Stay current on purpose — not only when the internet is on fire.
