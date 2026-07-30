---
title: Secure Defaults
published: true
hide:
- navigation
- toc
description: Designing secure defaults for tools and libraries — fail closed, least
  privilege, dangerous features opt-in, and interfaces that make the safe path the
  easy path.
tags:
- Security
- Design
---

# Secure Defaults: Making the Safe Path the Easy Path

Users will keep the defaults. Attackers know that. Secure defaults are not about scaring people — they are about shipping behaviour that stays safe when nobody reads the manual.

This matters especially for CLIs and libraries, where a convenient flag can become a permanent foot-gun.

## 1. Fail Closed When Unsure

If authentication is misconfigured, deny access. If a certificate cannot be verified, do not silently skip verification. If a path looks unsafe, refuse.

Failing open feels friendly until it is catastrophic. Reserve "continue anyway" for explicit, loud opt-ins.

## 2. Least Privilege by Default

Do not require root for tasks that work as a normal user. Do not open world-writable directories. Do not bind to all interfaces when localhost would do.

Ask for the minimum permissions needed for the common case. Document elevated modes separately.

## 3. Dangerous Features Are Opt-In

Examples that should never be on by default:

- Disable TLS verification
- Execute shell from untrusted input
- Overwrite files without confirmation in interactive tools (or without `--force` in scripts)
- Load plugins from arbitrary paths
- Log secrets at debug level

Name the flag after the risk (`--insecure`, `--allow-untrusted`) so callers feel the trade-off.

## 4. Safe Output and Safe Logs

Defaults should not print private keys, tokens, or full credentials to stdout, logs, or crash reports. Redact. Truncate. Require an explicit dump mode for debugging.

## 5. Compatibility Versus Safety

Changing a default is a breaking change for someone. Prefer:

- New major version when flipping a dangerous default
- Warnings in the old behaviour for one release cycle
- Migration notes that say *why* the default moved

Shipping a secure default late is still better than never — just version it honestly.

## 6. Document the Sharp Edges

Secure defaults fail if people disable them blindly to "make it work." Explain the safe configuration next to the error message. Link to a short troubleshooting section. Make compliance easier than bypass.

## 7. Closing Thoughts

Secure defaults are product design. The easy path should be the safe path; danger should require intent. Do that and most of your users are protected without becoming security experts.
