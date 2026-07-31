---
title: The Cybersecurity Rainbow
published: true
publish_date: "2026-07-02"
hide:
- navigation
- toc
description: A map of the colour-coded cybersecurity teams. Red, Blue, Purple, Green,
  Yellow, Orange, and White, what each one is responsible for, and how they fit
  together into one security programme.
tags:
- Security
- Ops
---

# The Cybersecurity Rainbow

Security work gets divided by colour. Red attacks, Blue defends, and five more teams cover the parts those two miss. The labels are a convenient shorthand for who owns which slice of the problem, and the useful thing about the full set is seeing the gaps between them.

Most organisations do not staff all seven. Treat this as a map of the responsibilities, not a hiring plan.

## Red Team: The Attackers

The Red Team plays the adversary. Its members are skilled in penetration testing, social engineering, and advanced hacking techniques, and the job is to mimic real-world attacks against your defences until something gives.

In practice that means reconnaissance, exploiting vulnerabilities, moving through networks to gain unauthorised access, and escalating privileges. The deliverable is a detailed report: what they found, how they exploited it, and what to do about it. That report is where the value is, and it tells you which weak points a real attacker would have reached first.

Red Team versus Blue Team exercises get their own article. This is the summary.

## Blue Team: The Defenders

The Blue Team defends the infrastructure. It monitors, detects, and responds, using security information and event management (SIEM) systems, intrusion detection systems (IDS), and firewalls to turn odd activity into an alert somebody acts on.

The rest of the work is quieter: building solid defences, running regular vulnerability assessments, and applying patches and updates to keep the easy wins away from attackers. Blue also owns the incident response plan, writing it and refining it, so that when something is detected the response is a procedure rather than an improvisation.

## Purple Team: The Collaborators

Purple is less a team than an arrangement. It puts Red and Blue in the same room so attack insights feed defensive improvements directly, instead of arriving weeks later as a document.

During a Purple exercise, both sides share findings and discuss attack methods as they go. The Blue Team learns detection and response against techniques it has just watched succeed, which is a much faster feedback loop than a report and a follow-up meeting.

## Green Team: The Builders

Green pushes security into the software development lifecycle, the DevSecOps end of the work. Secure coding standards, automated testing, secure architecture, code review, and dependency management, with tools like static application security testing (SAST) catching vulnerabilities early.

The team works alongside developers and engineers so security is part of the development workflow rather than a review stage at the end. Fewer vulnerabilities reach production, which means fewer for Blue to defend against.

## Yellow Team: The Educators

Yellow handles awareness and training for everyone in the organisation, not just the technical staff. Phishing, social engineering, and password practice, taught to the people attackers actually target.

The work is training programmes, workshops, newsletters, posters, and online courses, usually built with input from the other colour teams so the content reflects current attack techniques rather than last decade's. Done well, it turns the largest source of human error into the first line of defence. Most successful intrusions still start with someone clicking something, which is why this team matters more than its budget usually suggests.

## Orange Team: The Secure Designers

Orange sits between Green's secure development and Blue's defensive operations, and owns secure design. It puts security into the architecture of systems, networks, and applications before any of it is built.

The main activity is threat modelling: identifying risks during the design phase and making sure controls are part of the architecture from the outset. Orange works with developers, architects, and engineers, and its output is design decisions rather than code or alerts. It is Security by Design as a staffed function, and it prevents the vulnerabilities the other teams would otherwise spend their time finding.

## White Team: The Overseers

White runs the exercise. It sets the rules of engagement, defines the objectives, and keeps everything fair, in scope, and safe. During a Red versus Blue exercise, White referees: monitoring activity, checking both teams stay within the agreed boundaries, and mediating disputes so the simulation does not compromise the security it is meant to test.

Afterwards White facilitates the debrief and post-mortem, collecting insights from Red, Blue, and Purple, documenting the lessons, and following up on the improvements. Without that last part an exercise is entertainment.

## Closing Thoughts

The seven colours split into three groups. Red and Blue test the running system against each other. Green and Orange build security in during development and design. Yellow trains the people, Purple keeps the feedback flowing, and White makes sure the exercises produce evidence instead of anecdotes.

You almost certainly do not need seven teams. You do need to know which of those responsibilities nobody currently holds, because that is where your next incident starts.
