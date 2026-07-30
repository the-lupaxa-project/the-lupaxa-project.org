---
title: CLI Design
published: true
hide:
- navigation
- toc
description: Practical CLI design for open-source tools — flags and arguments, exit
  codes, stdout versus stderr, helpful errors, and interfaces that feel good in scripts
  and human hands.
tags:
- Engineering
- Tools
---

# CLI Design: Interfaces for Scripts and Humans

A command-line tool is an API that people type. Good CLIs disappear into muscle memory and shell scripts. Bad CLIs invent surprises: wrong exit codes, banners on stdout, flags that mean different things on Tuesdays.

This article collects practical defaults for small tools — the kind Lupaxa builds.

## 1. Make the Happy Path Short

The most common task should need the fewest keystrokes. Put advanced power behind explicit flags, not behind mandatory ceremony.

- Sensible defaults beat mandatory config files
- Subcommands should map to verbs users already say
- `--help` should be complete enough to avoid a docs hunt for basics

## 2. Flags, Arguments, and Predictability

Conventions help:

- **Arguments** for primary inputs (files, URLs)
- **Flags** for options and modes
- **Long flags** for clarity (`--output`), short flags for high-frequency use (`-o`)
- Prefer `--foo / --no-foo` over cryptic tri-state flags

Once you publish a flag name, changing it is a breaking change. Choose boring names.

## 3. Exit Codes Are Part of the Interface

Scripts branch on exit status.

Typical pattern:

- `0` — success
- non-zero — failure
- Distinct codes for distinct failure classes when scripts need them (optional, document them)

Never exit `0` after a failed operation because you printed an error nicely.

## 4.Stdout Versus Stderr

A simple rule:

- **stdout** — the actual result (data a pipe should receive)
- **stderr** — diagnostics, progress, errors, help

If your tool prints a success banner to stdout, you have broken `tool | jq`. Quiet by default; verbose on request.

## 5. Errors Should Teach the Next Step

Bad error: `Error: failed`

Better error:

- What failed
- Which input was involved (without leaking secrets)
- What to try next, when obvious

Colour and emoji are optional. Clarity is not.

## 6. Design for Automation

Assume someone will run your tool in CI:

- Support non-interactive modes
- Avoid prompts unless explicitly requested
- Provide machine-readable output modes when useful (`--json`)
- Keep output stable enough to parse — or version the format

## 7. Closing Thoughts

CLI design is empathy under constraint: few keystrokes, honest exit codes, clean pipes, and errors that shorten debugging. Get those right and your tool feels professional long before it grows a GUI.
