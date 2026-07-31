---
title: The Optimisation Trap
published: true
publish_date: "2026-07-09"
hide:
- navigation
- toc
description: Why capable engineers waste time polishing things that should not exist,
  how to tell warranted optimisation from busywork, and how first principles thinking
  keeps improvements pointed at something that matters.
tags:
- Engineering
- Mindset
---

# The Optimisation Trap: Making the Wrong Things Better

Elon Musk once said, *"The most common error of a smart engineer is to optimize a thing that should not exist."* It lands because the failure mode is so comfortable. Tuning a slow function feels like progress. Asking whether the function needs to exist feels like admitting the last three weeks were wasted.

Optimisation is not the problem. Optimising without first checking the target is.

## 1. Optimising the Wrong Thing Costs Twice

You lose the time you spend, and you leave behind more complexity to maintain. Worse, the optimised code now looks load-bearing, so the next person is even less likely to delete it.

Common ways engineers end up there:

- **Legacy code:** it has been in the codebase for years, so it feels essential. Longevity is not the same as importance.
- **Feature bloat:** features accumulate, and each one gets attention on its own terms rather than being weighed against user needs.
- **Sunk cost:** money and effort already spent become the argument for spending more, even when the feature stopped earning its place.
- **Incrementalism:** shaving milliseconds is easier than rethinking the design, so the bigger opportunity never gets considered.

## 2. Ask Whether It Should Exist

Before you tune anything, run through four questions:

- Does this feature add value for the user?
- Is this system critical to what the application actually does?
- Are we maintaining code that current or planned work does not need?
- Is there a simpler way to solve the problem?

If the honest answers point at deletion, delete. A smaller codebase is faster than a well-optimised large one.

## 3. When to Say No

### Features Almost Nobody Uses

Feature bloat usually comes from trying to satisfy every request or match a competitor's list. If only a sliver of users touch a feature, removing it beats optimising it. Fewer moving parts, less to maintain.

### Hypothetical Scale

Planning for growth is sensible. Building for a data volume you have no evidence you will reach is not. Optimising for imaginary scale leaves you with convoluted code that is harder to debug today in exchange for a benefit that may never arrive. Solve for realistic needs and revisit when the numbers move.

### Premature Optimisation

As Donald Knuth put it, *"Premature optimization is the root of all evil."* Refining performance before you know where the bottlenecks are is guessing with extra steps. Write clear, maintainable code first, get it working, then profile and target what the profiler shows you.

## 4. First Principles as a Filter

First principles thinking means breaking a problem down to its fundamentals and rebuilding from there. Applied to optimisation, it is a way of testing whether the thing deserves to exist:

- **Define the problem.** Name what the system or feature is meant to solve. Vague purpose produces vague optimisation.
- **Question the assumptions.** Is there a simpler route to the same outcome? Could this be removed entirely?
- **Rebuild from the requirements.** Start from what is essential rather than from what is currently there, and you often end up with something smaller.

## 5. How to Optimise When It Is Worth It

### Profile Before You Touch Anything

Use `Chrome DevTools` for front-end performance, `JProfiler` for Java, or `VisualVM` to find where time actually goes. Measured bottlenecks keep your effort data-driven instead of intuition-driven.

### Aim at Core Functionality

Optimise the paths users hit constantly or that the product depends on. Background processes and rarely used features can usually stay as they are unless they cause real problems.

### Refactor for Simplicity

Not every performance problem needs a performance fix. Complicated code is often a hint that the design is wrong, and simplifying it makes future optimisation easier. `SonarQube` can point at areas worth refactoring.

### Keep Dependencies Lean

Every library you pull in adds surface area to understand, update, and keep compatible. Fewer dependencies means less overhead and a codebase you can reason about when you do need to make it fast.

## 6. Closing Thoughts

Efficiency is a habit worth having, but it needs a target. Question what you are building before you polish it, apply first principles to decide whether it should exist at all, and profile before you optimise. The goal is not making things better. It is making the right things better.
