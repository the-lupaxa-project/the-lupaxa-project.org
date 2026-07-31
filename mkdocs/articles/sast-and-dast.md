---
title: SAST and DAST
published: true
publish_date: "2026-08-01"
hide:
- navigation
- toc
description: What static and dynamic application security testing each catch, why
  they find different bugs, and how to run SAST in CI and DAST against a deployed
  environment without drowning the team in findings.
tags:
- Security
- Engineering
---

# SAST and DAST: Two Views of the Same Application

Two scanners, two vantage points. Static Application Security Testing (SAST) reads your code without running it. Dynamic Application Security Testing (DAST) attacks your application without reading it. Neither finds everything the other does, which is why the usual answer is both.

Vulnerabilities that survive to production cost you data, money, and reputation. These two practices are how you find them earlier than that.

## SAST: Reading the Code

SAST is a white-box method. It analyses source code, bytecode, or compiled binaries without executing the application, examining structure and logic for vulnerabilities, code quality problems, and departures from secure coding practice. Because it only needs the code, it can run as soon as someone writes or edits a line.

### What It Looks For

SAST tools scan the codebase for known-bad patterns:

- **SQL injection:** unsanitised input reaching a query where an attacker could rewrite it.
- **Cross-site scripting:** paths that let attacker-controlled script into a web page.
- **Buffer overflows:** writes past the end of an allocated buffer, which crash at best and get exploited at worst.
- **Hardcoded secrets:** passwords, API keys, and tokens committed into the source.

The output is a report of what it found, before the application is compiled or tested anywhere live. That is the appeal: the vulnerability never reaches an environment where somebody could use it.

## DAST: Attacking the Running Application

DAST is a black-box method. It ignores the code and probes a running application from the outside, the way a user or an attacker would, watching how it responds. That means it needs somewhere deployed, usually a test environment or staging server, which puts it later in the lifecycle than SAST.

### What It Looks For

DAST tools interact with the live application and check what comes back:

- **SQL injection and XSS:** the same classes SAST hunts for, found from the other side by submitting malicious input and analysing the response.
- **Authentication and authorisation flaws:** weak session management, weak password policy, and the rest of the login surface.
- **Insecure configuration:** misconfigurations such as error messages that hand attackers detail about the system.
- **API weaknesses:** excessive data exposure, missing input validation, and similar gaps in endpoints.

You get a report in the same shape as SAST's, detailed enough to fix things, arriving before release rather than before build.

## Why You Want Both

### They Catch Different Things at Different Times

SAST scans the codebase directly and catches issues early, when they are cheapest and easiest to fix, before anything is built or deployed. DAST tests the application in its runtime environment and catches what only appears during execution: configuration errors, runtime behaviours, and the problems static analysis cannot see. Between them you cover the code level and the operational level.

### Early Fixes Cost Less

A flaw fixed during development is far cheaper than the same flaw fixed after deployment, and the gap widens at every stage the bug survives. Putting both scanners in the development process is how you resolve things before production instead of paying for them afterwards.

### Compliance Wants Evidence

Plenty of industries mandate secure development practice. SAST and DAST help you meet standards such as the `OWASP Top Ten`, `PCI-DSS`, and `ISO/IEC 27001` by identifying and addressing the risks those standards care about, and by giving you something concrete to show.

### Attackers Are Looking Anyway

New security risks appear regularly and attackers keep scanning for them. Finding your own problems first is the cheap version of that conversation. It protects sensitive data, customer trust, and reputation, none of which recover quickly.

## Wiring Them Into the Pipeline

### SAST Belongs in CI

Run SAST automatically whenever a developer commits, so code is checked continuously rather than during an occasional security push. `SonarQube`, `Checkmarx`, and `Fortify` all slot into a CI/CD pipeline, giving developers immediate feedback and keeping flawed code out of the main branch.

### DAST Belongs in a Deployed Environment

DAST needs a running application, so point it at a test or staging environment where the app is fully deployed and you can attack it without consequences. `OWASP ZAP`, `Burp Suite`, and `Acunetix` are the usual choices. Run them as a pipeline stage or on a schedule, but run them before the release goes out.

### Together, Not Instead

SAST works from the inside on the code. DAST works from the outside on the running system. Combined they find a broader range of vulnerabilities than either manages alone, which is the whole argument for running both.

### Shift Left, and Keep Going

DevSecOps builds security into the DevOps process rather than bolting it on at the end, the *"shift-left"* idea of testing early and often. Putting SAST and DAST into that pipeline makes security part of how the team works instead of a gate they resent, and a team that expects security feedback writes safer code before the scanner asks.

## Closing Thoughts

SAST and DAST answer different questions. Is this code dangerous? Is this deployment attackable? Run both and you cover vulnerabilities at the code level and the operational level, early enough that fixing them stays cheap and quiet.

The pitch is not that scanners make you secure. It is that they shrink your list of unknowns on your schedule, before somebody else goes looking.
