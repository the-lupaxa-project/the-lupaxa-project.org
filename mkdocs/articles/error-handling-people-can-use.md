---
title: Error Handling People Can Use
published: true
publish_date: "2026-07-30T16:03:17"
hide:
- navigation
- toc
description: Practical error handling for CLIs and libraries. Clear messages, exit
  codes, retries, typed failures, and when to crash versus recover.
tags:
- Engineering
- Tools
---

# Error Handling People Can Use: Failures That Teach

Errors are part of the interface. A stack trace dumped on a new user is a failed conversation. A precise message with a next step is product quality.

This article focuses on CLIs and small libraries, where error handling is often the difference between adoption and abandonment.

## Say What Failed and What to Try

Useful errors include:

- What operation failed
- Which input or resource was involved (without secrets)
- A plausible next step when one exists

"Error: failed" trains people to ignore you. "Cannot read key file `/path`: permission denied. Check ownership, or run without elevated paths you cannot access" teaches.

## Exit Codes Are for Scripts

Reserve `0` for success. Use non-zero for failure. If you expose distinct codes, document them. Scripts should not scrape stderr to decide what happened if a code would do.

## Choose Crash Versus Recover Deliberately

Crash (or return a hard error) when continuing would corrupt state or hide danger. Recover when the failure is expected and local, like a missing optional file, an empty search result, or a retryable network blip.

Infinite silent retries are not recovery. They are a hang.

## Retries Need Budgets

If you retry:

- Cap attempts
- Back off
- Surface the last error
- Make retries optional or visible in verbose mode

Libraries should usually let the caller decide retry policy.

## Typed Errors Help Callers

For libraries, distinct error types or codes beat string matching. Callers can handle "not found" differently from "permission denied" without parsing English.

Keep messages human; keep structure machine-friendly.

## Log for Operators, Message for Users

Verbose logs can hold detail. The default user-facing message should stay short. Do not dump internal tracebacks unless `--debug` is on.

## Closing Thoughts

Error handling is empathy under failure. Clear messages, honest exit codes, deliberate retries, and typed failures turn broken runs into solvable problems, which is what users actually needed.
