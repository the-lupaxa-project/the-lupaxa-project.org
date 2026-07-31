---
title: mTLS and Client Certificates
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Mutual TLS and client certificates in practice. How they differ from
  ordinary HTTPS, when they are worth the trouble, and how small tools should issue
  and verify them.
tags:
- Security
- Certificates
---

# mTLS and Client Certificates: Proving Both Sides

Ordinary HTTPS proves the server's identity to the client. **Mutual TLS (mTLS)** also proves the client's identity to the server using a client certificate. That is powerful for machine-to-machine links, internal APIs, and agent-style tools. It is also easy to misconfigure.

## Server TLS Versus Mutual TLS

- **Server TLS:** client verifies the server certificate; server may still use passwords or tokens for the user.
- **mTLS:** both sides present certificates; the server authenticates the client by certificate (often *instead of* a shared password).

mTLS is identity in the handshake, not application logic sprinkled later.

## When Client Certificates Help

Good fits:

- Service-to-service calls inside a private network
- Device or agent authentication
- Admin APIs where you control certificate issuance
- Replacing long-lived static tokens with short-lived certs

Poor fits:

- Random browser users on the public internet (painful UX)
- Anything where you cannot distribute and revoke client certs

## What You Must Verify

On the server:

- Certificate chain trusts your issuing CA
- Certificate is within validity
- Name / SAN matches the expected client identity
- Key usage allows client authentication
- Revocation policy you can actually enforce

Skipping verification "to make it work" deletes the point of mTLS.

## Issuance and Renewal

Treat client certificates like keys with an expiry:

- Issue from a CA you control
- Prefer short lifetimes with automated renewal
- Record which identity owns which cert
- Revoke or stop trusting when access should end

Self-signed client certs pinned one-by-one do not scale; a small internal CA usually does.

## Tooling Habits

For CLIs and libraries:

- Make CA bundle and client cert/key paths explicit
- Refuse empty or world-readable key files when possible
- Surface handshake errors clearly (`certificate verify failed` with cause)
- Document a local mutual-TLS smoke test

## Tokens Still Have a Place

mTLS authenticates the channel identity. Authorisation (roles, scopes) may still live in the application. Do not confuse "has a valid client cert" with "may delete production."

## Closing Thoughts

mTLS is strong authentication for systems you operate. Issue carefully, verify strictly, renew on purpose. Use it where machines talk to machines, not where a password reset email would have been kinder.
