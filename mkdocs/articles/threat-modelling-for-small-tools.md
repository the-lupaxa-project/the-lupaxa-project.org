---
title: Threat Modelling for Small Tools
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Lightweight threat modelling for CLIs, libraries, and small services.
  Assets, attackers, trust boundaries, and a practical checklist without enterprise
  ceremony.
tags:
- Security
- Engineering
---

# Threat Modelling for Small Tools: Who Can Hurt Whom

Threat modelling sounds like a workshop with sticky notes and a facilitator. For a small open-source tool it can be a one-page habit: name what you protect, who might attack it, and where trust stops.

You do not need STRIDE bingo. You need clearer design decisions.

## 1. Start With Assets

Write down what would hurt if abused:

- Private keys, tokens, or credentials the tool touches
- User data it reads or writes
- Integrity of generated artefacts (certs, configs, packages)
- Availability of a service it exposes
- Reputation of maintainers if the tool becomes malware delivery

If nothing valuable is at stake, say so and move on. Most CLIs still touch *something*.

## 2. Draw Trust Boundaries Roughly

Ask where data crosses a line:

- User laptop → your process
- Your process → network
- Your process → filesystem
- Your library → calling application
- CI → package registry

Attacks love boundaries. So should your checks.

## 3. Name Realistic Attackers

Skip movie villains. Prefer:

- Malicious input from an untrusted file or URL
- A compromised dependency
- A curious user on a shared machine
- An automated scanner hitting a default port
- A contributor planting a sneaky PR

Design for the attackers you will actually meet.

## 4. Ask Four Questions

For each important flow:

1. What are we trusting?
2. What happens if that trust is wrong?
3. How would we notice?
4. What is the cheapest control that helps?

Controls might be: validate input, refuse unsafe defaults, verify signatures, drop privileges, or document "do not run as root."

## 5. Record Decisions, Not Decks

A short `SECURITY.md` section or architecture note beats a forgotten Confluence page:

- "We never send private keys over the network"
- "Config paths are user-controlled; we refuse world-writable key files"
- "Releases are signed; install docs show how to verify"

Future you will thank present you.

## 6. Revisit on Big Changes

New network calls, new privilege, new deserialisation, a new plugin system: those are threat-model events. A five-minute review at PR time is worth more than an annual ceremony.

## 7. Closing Thoughts

Threat modelling for small tools is disciplined curiosity: protect the valuable bits, distrust boundaries, and write down the non-negotiables. Do that and security stops being a vibe and becomes part of the design.
