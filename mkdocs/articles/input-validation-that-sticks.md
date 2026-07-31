---
title: Input Validation That Sticks
published: true
publish_date: "2026-01-22"
hide:
- navigation
- toc
description: Practical input validation for CLIs and small services. Paths, URLs,
  subprocesses, sizes, and the failure modes that let an attacker steer your tool.
tags:
- Security
- Engineering
---

# Input Validation That Sticks: Don't Become an Exploit Gadget

Most security bugs in small tools are not exotic crypto failures. They are trust in strings: paths, URLs, hostnames, and shell fragments that an attacker influences. Validation that sticks happens at every trust boundary, not once as a regex at the front door.

## 1. Name the Untrusted Inputs

List them:

- CLI arguments and flags
- Environment variables
- Config files
- Files whose paths come from users
- HTTP responses and webhooks
- Plugin or extension names

If it crossed a boundary, it is untrusted until proven otherwise.

## 2. Paths: Contain Them

Path traversal (`../../etc/passwd`) still works when you naively join user strings to a base directory.

- Resolve to a canonical path
- Ensure the result stays under an allowed root
- Refuse unexpected symlinks when that is your threat model
- Do not shell out with user paths unquoted

## 3. URLs and Network Targets

User-supplied URLs invite SSRF: your tool fetches internal metadata endpoints or localhost admin ports.

- Allow-list schemes (`https` only when possible)
- Block link-local and metadata ranges when fetching on behalf of users
- Cap redirects
- Set timeouts

"Just curl whatever they gave us" is a feature request from attackers.

## 4. Commands and Shells

If you must run subprocesses:

- Prefer argument arrays over shell strings
- Never interpolate untrusted input into `shell=True`
- Allow-list executables when the command is selectable

Command injection is almost always a design smell, not bad luck.

## 5. Validate Types Early

Parse ints, enums, hostnames, and PEM blocks with strict parsers. Reject unknown fields in configs. Fail with a clear error pointing at the bad value.

Silent coercion hides attacks and bugs alike.

## 6. Test the Nasty Cases

Add fixtures for `../`, weird unicode dots, newlines in arguments, oversized inputs, and file:// URLs. Security tests are just tests that remember adversaries.

## 7. Closing Thoughts

Input validation that sticks treats every boundary as hostile until proven kind. Contain paths, tame URLs, avoid shells, parse strictly. Do that and your CLI stays a tool instead of becoming someone else's gadget.
