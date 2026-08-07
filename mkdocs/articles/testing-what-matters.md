---
title: Testing What Matters
published: true
publish_date: "2026-07-30T14:04:44"
hide:
- navigation
- toc
description: Why high coverage can be a vanity metric, how to test behaviour instead
  of mocks, and how small open-source projects can build a test suite that catches
  real regressions without drowning contributors.
tags:
- Engineering
- Testing
---

# Testing What Matters: Beyond Vanity Coverage

Test suites exist to protect behaviour users care about. They do not exist to decorate a README with `100% coverage`. When tests only exercise mocks, they congratulate the suite for inventing a fake world, and then production discovers the real one.

This article is about testing that earns its keep, especially in small projects.

## Coverage Is a Clue, Not a Score

Coverage answers: "Which lines ran?" It does not answer: "Would we notice a bad change?"

High coverage with weak assertions is theatre. Low coverage on a tiny critical path with sharp tests can be excellent engineering.

Use coverage to find *untested risk*, not to chase a number.

## Prefer Behaviour Over Implementation

Behavioural tests describe outcomes:

- Given this input, the CLI exits `0` and prints this
- Given a bad flag, we get a clear error on stderr
- Given this API call, the library returns this shape

Implementation tests bind you to private structure:

- Asserting which private method was called
- Replicating internal call graphs with mocks
- Snapshotting incidental formatting forever

When the design improves, behaviour tests still help. Implementation tests mostly fight you.

## Mocks Are Tools, Not a Lifestyle

Mocks are useful at boundaries you do not control: network, time, third-party APIs. They are overused when they replace your own modules so thoroughly that nothing real remains.

A warning sign: every test file begins by mocking the system under test's neighbours until the test can only pass by confirming your stubs were wired.

Prefer:

- Fakes and fixtures you own
- Temporary directories and sample files
- Contract tests at the edges

## Design for Testability Without Ceremony

Small projects can stay testable by:

- Keeping pure functions pure
- Isolating I/O
- Making clocks and randomness injectable when they matter
- Shipping example inputs as fixtures

You do not need a grandiose architecture diagram to make a function testable.

## Make Failures Obvious

A good failing test names the behaviour that broke. A bad one dumps a stack and a puzzle.

Invest in:

- Clear test names
- Assertions with useful messages
- Deterministic ordering and seeds
- CI that runs the same commands developers run locally

Flaky tests train teams to ignore red builds. Delete or fix them quickly.

## Right-Size the Suite

Not every idea needs an integration palace. Aim for a pyramid that matches the project:

- Many fast unit tests for logic
- Fewer tests for CLI/module boundaries
- A small number of end-to-end checks for critical journeys

For libraries, public API tests matter most. For CLIs, exit codes and output contracts matter most.

## Closing Thoughts

Test what users would curse you for breaking. Let coverage reports guide curiosity, not vanity. A modest suite that fails for the right reasons is worth more than a green cathedral of mocks.
