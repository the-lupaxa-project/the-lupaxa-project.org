---
title: Error Handling People Can Use
published: true
hide:
- navigation
- toc
description: Practical error handling for CLIs and libraries — clear messages, exit
  codes, retries, typed failures, and when to crash versus recover.
tags:
- Engineering
- Tools
---

# Error Handling People Can Use: Failures That Teach

Errors are part of the interface. A stack trace dumped on a new user is a failed conversation. A precise message with a next step is product quality.

This article focuses on CLIs and small libraries — where error handling is often the difference between adoption and abandonment.

## 1. Say What Failed and What to Try

Useful errors include:

- What operation failed
- Which input or resource was involved (without secrets)
- A plausible next step when one exists

"Error: failed" trains people to ignore you. "Cannot read key file `/path`: permission denied — check ownership or run without elevated paths you cannot access" teaches.

## 2. Exit Codes Are for Scripts

Reserve `0` for success. Use non-zero for failure. If you expose distinct codes, document them. Scripts should not scrape stderr to decide what happened if a code would do.

## 3. Choose Crash Versus Recover Deliberately

Crash (or return a hard error) when continuing would corrupt state or hide danger. Recover when the failure is expected and local — missing optional file, empty search result, retryable network blip.

Infinite silent retries are not recovery. They are a hang.

## 4. Retries Need Budgets

If you retry:

- Cap attempts
- Back off
- Surface the last error
- Make retries optional or visible in verbose mode

Libraries should usually let the caller decide retry policy.

## 5. Typed Errors Help Callers

For libraries, distinct error types or codes beat string matching. Callers can handle "not found" differently from "permission denied" without parsing English.

Keep messages human; keep structure machine-friendly.

## 6. Log for Operators, Message for Users

Verbose logs can hold detail. The default user-facing message should stay short. Do not dump internal tracebacks unless `--debug` is on.

## 7. Closing Thoughts

Error handling is empathy under failure. Clear messages, honest exit codes, deliberate retries, and typed failures turn broken runs into solvable problems — which is what users actually needed.
