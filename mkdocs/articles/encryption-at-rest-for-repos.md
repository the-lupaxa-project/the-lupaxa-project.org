---
title: Encryption at Rest for Repos
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Encrypting secrets inside Git repositories. When git-crypt and similar
  tools help, where key management goes wrong, and safer patterns for small teams.
tags:
- Security
- Git
---

# Encryption at Rest for Repos: Keeping Secrets Out of Plain Git

Git is excellent history and a terrible place for plaintext secrets. Encryption-at-rest tools such as `git-crypt` let you store sensitive files in a repository while keeping the blobs unreadable to anyone without a key. Used well, they reduce accidental leaks. Used carelessly, they create a false sense of safety.

This is for small teams shipping tools that need shared encrypted config, without standing up a full enterprise vault on day one.

## What Problem This Solves

You need a file in the repo (or next to it in the workflow) that:

- Must travel with the project
- Must not be readable in clones, forks, or leaked archives
- Can be decrypted by a defined set of people or CI identities

Examples: environment templates with real values for staging, API tokens for integration tests, customer-specific overlays.

## What It Does Not Solve

Encrypted-in-git is not:

- A substitute for proper secret stores in production
- Protection against a compromised developer laptop that has the key
- Safe if you commit the key beside the ciphertext
- A fix for secrets already in history, which need rotating instead

If the decrypt key is world-readable in CI logs, you encrypted nothing that matters.

## Pick a Narrow Set of Files

Encrypt only what must be shared as files. Prefer environment injection from a vault or CI secrets for runtime credentials.

Mark paths explicitly (for example via `.gitattributes`). Review that list in PRs. Encrypting "everything under `config/`" invites surprises.

## Key Management Is the Real Product

Decide:

- Who can decrypt?
- How do you add or remove people?
- How do you rotate after a laptop loss?
- How does CI get the key without printing it?

Document the ceremony. Untested key recovery is not a plan.

## CI Patterns That Work

- Store the unlock key in a protected CI secret
- Decrypt only on jobs that need it
- Never upload decrypted artefacts to public logs
- Fail closed if unlock fails

Keep decrypt steps boring and identical across environments.

## Operational Habits

- Rotate when someone leaves the project
- Audit who has keys periodically
- Keep a break-glass path owned by more than one person
- Treat plaintext working copies as sensitive disks

## Closing Thoughts

Repo encryption is a scalpel: useful for a few shared files, dangerous as a general secret strategy. Encrypt narrowly, guard keys like production credentials, and still prefer proper secret stores when the system grows up.
