---
title: Deprecation Without Chaos
published: true
hide:
- navigation
- toc
description: How to deprecate APIs and flags calmly — warnings, timelines, SemVer,
  migration paths, and removing old behaviour without surprising your users.
tags:
- Open Source
- Engineering
---

# Deprecation Without Chaos: Changing APIs Without Burning Trust

Software has to change. Deprecation is how you change without blindsiding people. Done well, users migrate. Done poorly, they pin forever and curse your majors.

This pairs with semantic versioning: deprecation is the social process; SemVer is the numbering.

## 1. Deprecate Before You Delete

Never remove a public flag, function, or config key in a minor release without a prior warning period — unless you are still in `0.x` and have said so clearly.

Sequence that works:

1. Mark deprecated (docs + runtime warning)
2. Ship at least one release where both old and new work
3. Remove in a major (or announced `0.x` break)

## 2. Warn Where Developers Will See It

Documentation alone is not enough.

- CLI: stderr warning when the old flag is used
- Library: deprecation warning once per process (not a flood)
- Config: message at load time naming the replacement

Include the replacement in the warning. "Deprecated" without "use X instead" is just noise.

## 3. Give a Timeline People Can Plan Around

Say which version will remove the behaviour, or "will be removed in the next major." If you cannot commit to a date, commit to a version gate.

Silence followed by a sudden break feels like betrayal even when SemVer allows it.

## 4. Make Migration Cheap

Provide:

- A one-to-one replacement when possible
- A short migration snippet in the changelog
- Compatibility shims for one major when the cost is low

The goal is conversion, not punishment.

## 5. Track Deprecations Visibly

Keep a small "Deprecated" section in the changelog or docs. Maintainers forget; users search. A living list prevents zombie APIs that linger forever without removal *or* support.

## 6. Resist Eternal Compatibility

Endless shims become a second product. After the announced major, remove the old path. People who need the old behaviour can stay on the old major — that is what majors are for.

## 7. Closing Thoughts

Deprecation without chaos is courtesy plus SemVer: warn early, guide clearly, remove on purpose. Change the system without training users to fear every upgrade.
