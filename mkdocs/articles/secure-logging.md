---
title: Secure Logging
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: Practical secure logging for tools and services. What never to log,
  redaction, crash reports, debug flags, and keeping observability from becoming a
  leak.
tags:
- Security
- Engineering
---

# Secure Logging: Observability Without the Leak

Logs help you debug. They also become a second database of secrets if you are careless. Secure logging is the discipline of recording enough to operate while refusing to become an accidental secret store.

## Decide What Must Never Appear

Default deny for:

- Passwords, API tokens, session cookies
- Private keys and key material
- Full authorisation headers
- Personal data you are not allowed to retain
- Raw payment or health payloads

If debug mode needs them, require an explicit unsafe flag and keep it off in CI defaults.

## Redact at the Boundary

Centralise redaction helpers. Do not rely on every call site remembering `password=`. Prefer structured logs with known fields so redaction can target keys reliably.

When in doubt, hash or truncate identifiers instead of printing full credentials.

## Crash Reports Are Logs Too

Unhandled exceptions often serialise request objects, configs, or environment maps. Review what your crash reporter captures. Scrub before upload. Local `--debug` dumps should stay local.

## Levels Are a Control

- `info`/`warn`: safe operational events
- `debug`: denser detail, still scrubbed
- Unsafe dumps: explicit opt-in only

Shipping with debug enabled in production is a configuration bug with security consequences.

## Who Can Read Logs?

Access control matters. Shared Slack channels, public CI logs, and world-readable S3 buckets turn careful code into a leak. Treat log sinks with the same seriousness as databases that hold customer data.

## Retention and Deletion

Keep logs long enough to investigate, not forever by default. Know how to purge when a secret *did* slip through, and rotate the secret anyway.

## Closing Thoughts

Secure logging is restraint: redact by default, protect sinks, and make dangerous verbosity opt-in. You can still see what broke without mailing the keys to everyone who can open a log viewer.
