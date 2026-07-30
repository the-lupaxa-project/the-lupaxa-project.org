---
title: The Optimisation Trap
published: true
hide:
- navigation
- toc
description: Discover how to avoid the optimisation trap in software engineering.
  Learn why it's essential to focus on purpose-driven improvements, inspired by Elon
  Musk's insights on building the right things, not just better things.
tags:
- Engineering
- Mindset
---

# Avoiding the Optimisation Trap in Software Engineering: Lessons from Elon Musk

Elon Musk once said, *"The most common error of a smart engineer is to optimize a thing that should not exist."* For software engineers, this is a reminder to question assumptions and think critically about the value of the systems, features, and processes we work on. Too often, we can fall into the trap of optimising code, algorithms, or features that don't meaningfully contribute to the software's core goals. Instead of making incremental improvements to things that may not even be necessary, we should step back and consider whether we're addressing the right problems in the first place.

Let's explore why it's important to avoid unnecessary optimisation in software engineering, how to recognize when optimisation is warranted, and the strategies we can employ to make purpose-driven improvements.

## 1. The Perils of Optimising the Wrong Things

Software engineering thrives on efficiency, and the drive to optimise is one of the field's cornerstones. However, this drive can become counterproductive when applied to the wrong things. Optimising unnecessary features or inefficient code that doesn't serve a purpose can lead to wasted time, increased complexity, and a diversion from the software's primary goals. In the worst cases, unnecessary optimisation can result in software bloat and reduced maintainability.

There are a few common reasons why engineers fall into this optimisation trap:

- **Legacy Code:** Teams often spend time optimising legacy code that is no longer critical to the software's core function. Legacy code can feel indispensable due to its long-standing presence in the codebase, but it may no longer be necessary.
- **Feature Bloat:** Adding extra features over time can result in a bloated application. Engineers might optimise each of these features without questioning whether they are still relevant or aligned with user needs.
- **Sunk Cost Fallacy:** Time and resources that have already been invested in a system or feature may prompt further optimisation simply to justify the initial investment, even if the feature no longer adds value.
- **Incrementalism Over Innovation:** Optimising small details can distract from broader opportunities for innovation. Focusing on incremental improvements often means missing the chance to rethink or redesign the system with a more effective solution.

## 2. Focusing on Purpose-Driven Optimisation

Rather than automatically seeking to optimise existing systems, engineers should consider the purpose and value of the software they're building. Software engineers need to regularly ask:

- Does this feature add value for the user?
- Is this system critical to the application's core functionality?
- Are we spending time on code that isn't necessary for current or future needs?
- Are there simpler, more efficient ways to solve this problem?

By focusing on purpose-driven optimisation, software engineers can prioritize meaningful improvements that align with user needs and the application's goals. This approach promotes a lean and effective codebase rather than one that is weighed down by unnecessary complexity.

## 3. Avoiding Over-Optimisation: When to Say No

It can be tempting to optimise every aspect of a codebase, but knowing when to avoid optimisation is a valuable skill for any software engineer. Here are a few scenarios where stepping back from optimisation can lead to better results:

### Unnecessary Features

Feature bloat occurs when software has more functionality than is necessary, often due to a desire to address a wide range of user needs or to differentiate from competitors. But not every feature requires deep optimisation. For instance, if a product contains a feature that only a small subset of users utilizes, it may be better to remove the feature entirely rather than continually optimising it. This helps maintain a clean and focused codebase.

### Over Engineering for Hypothetical Scenarios

Engineers often optimise code in anticipation of future needs or increased scale. While planning for growth is essential, optimising for scenarios that may never happen can lead to unnecessary complexity. For example, optimising for a hypothetical data scale far beyond the current requirements can introduce convoluted code, making it harder to maintain and debug. Instead, it's best to focus on realistic needs and revisit optimisation when necessary.

### Premature Optimisation

Premature optimisation is a well-known pitfall in software development. Spending time refining code for performance before you understand the application's actual bottlenecks often results in wasted effort. As Donald Knuth famously said, *"Premature optimization is the root of all evil."* Instead of immediately optimising, focus on creating clear and maintainable code first. Once you have a functioning application, use profiling tools to identify performance bottlenecks and target optimisation efforts there.

## 4. Applying First Principles Thinking to Software Optimisation

Elon Musk often advocates for first principles thinking, a method of problem-solving that involves breaking down complex problems into their most fundamental components and building up from there. This approach is particularly valuable in software engineering, as it encourages us to question assumptions and look for simple, foundational solutions.

By applying first principles thinking, software engineers can better determine whether something should even exist before investing time in optimising it. Here's how to incorporate this approach into software development:

- **Define the Problem:** Identify the specific problem that the system or feature is intended to solve. Understanding the purpose helps ensure that optimisation efforts are aligned with the application's goals.
- **Question Assumptions:** Consider the assumptions underlying the system or feature. Is there a simpler way to achieve the same outcome? Could the system or feature be removed entirely?
- **Start from Scratch:** When faced with a complex problem, break it down to its fundamental requirements. By looking at what's essential, you can design a solution that is streamlined and avoids unnecessary complexity.

## 5. Strategies for Purpose-Driven Optimisation

Once you've identified areas that genuinely benefit from optimisation, it's essential to implement changes thoughtfully. Here are strategies to help software engineers optimise effectively while keeping the bigger picture in mind:

### Profiling and Benchmarking

Use profiling and benchmarking tools to identify performance bottlenecks. Tools like `Chrome DevTools` (for front-end performance), `JProfiler` (for Java), or `VisualVM` can help you determine where your application is slowing down. By focusing on measurable performance issues, you ensure that your optimisation efforts are targeted and data-driven.

### Focus on Core Functionality

Optimise the parts of your application that impact core functionality. Features that users interact with frequently or that are critical to the application's success should be your primary focus. Non-essential features or background processes can often be left as-is unless they introduce significant issues.

### Refactoring for Simplicity

Instead of only focusing on performance, consider refactoring code to improve readability and simplicity. Complex code can often be a sign that you're optimising something unnecessarily. Cleaner code is easier to maintain and more straightforward to optimise when necessary. Tools like `SonarQube` can help identify areas for refactoring and offer suggestions for improvement.

### Minimize Dependencies

Each external library or dependency you include adds to your codebase's complexity and can make optimisation more challenging. Minimize dependencies to avoid the overhead associated with keeping them updated and compatible. Using a lean codebase with minimal dependencies makes it easier to optimise and manage in the long term.

## Closing Thoughts
Elon Musk's observation about the dangers of optimising things that shouldn't exist is a powerful reminder for software engineers to focus on purpose-driven improvements. In a field that emphasizes efficiency and performance, it's essential to remember that not every part of a system needs to be refined. By questioning the purpose of what we're building and applying first principles thinking, we can avoid unnecessary complexity and create software that is streamlined, maintainable, and genuinely valuable.

In the end, optimising with purpose means not just making things better but ensuring that we're making the right things better. By focusing on value-driven optimisation, software engineers can build products that serve users effectively, conserve resources, and avoid the common pitfalls of over-engineering and feature bloat.
