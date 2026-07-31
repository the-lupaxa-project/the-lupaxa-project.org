---
title: Config Design
published: true
hide:
- navigation
- toc
description: Practical configuration design for tools. Flags, environment variables,
  files, precedence, secrets, and defaults that stay understandable as projects grow.
tags:
- Engineering
- Tools
---

# Config Design: Flags, Env, Files, and Precedence

Configuration is how users shape behaviour without forking your code. Bad config design creates folklore ("set these six variables or it breaks"). Good config design is boring: predictable sources, clear precedence, and no secrets in the wrong place.

## 1. Three Common Sources

Most tools use some mix of:

- **Flags / arguments** apply per invocation, great for scripts and overrides
- **Environment variables** apply per process or deployment, good for hosts and CI
- **Config files** hold persistent project or user settings

Use each for what it is good at. Do not invent a fourth source without need.

## 2. Publish Precedence

Users need one rule, for example:

1. CLI flags win
2. Then environment variables
3. Then config file
4. Then built-in defaults

Document it once. Stick to it. Silent overrides are how people lose weekends.

## 3. Defaults Must Be Explained

Every default is a product decision. Put the important ones in the README or `--help`. If a default is dangerous, it should not be the default (see secure defaults).

## 4. Keep Secrets Out of Config Files in Git

Tokens and private keys belong in environment variables, secret stores, or permission-restricted files outside the repo. If a config file *can* hold a secret, document how to reference an external secret instead of pasting values.

Refuse to load world-readable key files when you can detect them.

## 5. Prefer Explicit Schemas

Validate early. Unknown keys should warn or error. Types should be checked. A typo in `timout` should not silently use the default timeout forever.

Generate example configs from the same schema you validate against when practical.

## 6. Design for Humans and Machines

- Human-friendly layered config for local use
- Machine-friendly env/flags for CI
- Stable names; renaming is a deprecation event

Avoid requiring both a file *and* twelve flags for the happy path.

## 7. Closing Thoughts

Config design is interface design. Clear sources, clear precedence, validated inputs, and secrets kept out of git will save more support time than any clever new format.
