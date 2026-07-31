---
title: Key Lifecycle
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: The key lifecycle for small security tools. Generate, distribute, rotate,
  revoke, and retire cryptographic keys and certificates without drama.
tags:
- Security
- Engineering
---

# Key Lifecycle: From Birth to Retirement

A key that never rotates is a key that eventually leaks in slow motion. Lifecycle thinking (generate, use, rotate, revoke, destroy) turns cryptography from a one-off setup step into something you can actually operate.

This applies to TLS keys, client certificates, signing keys, and API-adjacent secrets that behave like keys.

## 1. Generate Deliberately

- Use well-tested libraries and tools
- Choose algorithm and size/curves you can support for the lifetime
- Generate on a machine you trust; minimise copies
- Record what the key is *for* (purpose beats filename folklore)

One key per purpose beats a master key that unlocks everything.

## 2. Distribute Narrowly

Only the processes and people that need a private key should have it. Prefer:

- CI secrets / vault injection over email
- Separate keys per environment
- Read-restricted files with clear ownership

Distribution is where most "secure generation" dies.

## 3. Rotate on a Schedule, and on Events

Rotate when:

- The planned lifetime ends
- Someone with access leaves
- You suspect exposure
- A dependency or tool forced a weak format

Overlapping trust (old and new valid briefly) makes rotation calm. Big-bang cutovers make outages.

## 4. Revoke When Trust Ends

Certificates need CRL/OCSP or short lifetimes. Signing keys need published revocation or key retirement notices. Application secrets need invalidation at the provider.

If you cannot revoke, your lifetimes must be short enough that revocation is less critical.

## 5. Retire Cleanly

When a key is done:

- Remove it from vaults and disks
- Delete CI variables
- Update docs that still name it
- Keep audit notes of *when* and *why* it was retired

Forgotten keys in backups are still keys.

## 6. Automate the Boring Path

Humans forget anniversaries. Automate expiry alerts, renewal jobs, and "cert expires in 14 days" checks. Manual calendars fail during holidays.

## 7. Closing Thoughts

Cryptography fails operationally more often than mathematically. Own the lifecycle: generate carefully, distribute narrowly, rotate routinely, revoke when trust ends. Do that and your tools stay trustworthy as the people and machines around them change.
