---
title: Supply-Chain Signing
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Practical supply-chain signing for open-source releases. Checksums,
  signatures, provenance, and verification steps users can actually follow.
tags:
- Security
- Open Source
---

# Supply-Chain Signing: Proving What You Shipped

Dependency hygiene asks what you trust. Signing asks whether the artefact in front of you is the one the maintainer meant to publish. Together they shrink the space where malware and mirrors can lie.

You do not need a full enterprise SLSA programme on day one. You need verifiable releases and docs that show how to check them.

## Start With Checksums

Publish checksums (SHA-256 is fine) next to binaries and archives. Users can verify downloads. Automate generation in release CI so humans do not mistype hashes.

Checksums detect corruption and many dumb substitutions. They do not prove *who* produced the file unless the checksum list itself is authenticated.

## Sign the Artefacts You Care About

Common patterns:

- Sign release archives or binaries with a maintainer key
- Sign git tags
- Sign package registry publishes when the ecosystem supports it

Pick keys you can protect. A signature with a leaked key is theatre.

## Provenance When You Can

Provenance attests *how* something was built (which commit, which workflow). GitHub attestations and similar systems help bind artefacts to source. Use them when your release pipeline is already automated. They are a poor fit for hand-built mystery zips.

## Document Verification

A signature nobody knows how to check is decoration. In the README or release docs:

- What is signed
- Which key / identity to trust
- Exact commands to verify
- What success looks like

Keep the happy-path verify under a minute.

## Protect the Pipeline

Signing secrets belong in CI environments with tight access, not in the repository and not on every laptop. Separate who can merge from who can publish when the project grows.

Compromise of the release job is compromise of trust. Guard it accordingly.

## Be Honest About Scope

Signing your releases does not secure your dependencies' releases. Say what you guarantee. Point users at lockfiles and audits for the rest.

## Closing Thoughts

Supply-chain signing is evidence: checksums for integrity, signatures for authenticity, provenance for the build story. Automate it, document verification, and protect the keys. Then users can trust your bits on purpose instead of on hope.
