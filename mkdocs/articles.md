---
hide:
  - navigation
  - toc
---

<div class="filter-panel filter-panel--compact" data-article-filters markdown="0">
  <div class="filter-panel-search">
    <label for="article-search">Search articles</label>
    <input
      id="article-search"
      type="search"
      placeholder="Search by title, description, or tag"
      autocomplete="off"
      data-article-search
    />
  </div>
  <div class="filter-panel-select">
    <label for="article-category">Tag</label>
    <select id="article-category" data-article-category>
      <option value="">All tags</option>
    </select>
  </div>
  <div class="filter-panel-actions">
    <button
      type="button"
      class="md-button lupaxa-button filter-panel-clear"
      data-article-clear
    >
      Clear filters
    </button>
  </div>
  <div
    class="filter-panel-summary"
    aria-live="polite"
    data-article-summary
  >
    Showing all articles
  </div>
</div>

<div class="grid cards catalogue-grid catalogue-grid--articles" data-article-catalogue markdown>

-   **[Certificates Without the Jargon](articles/certificates-without-the-jargon.md)**

    ---

    ![Article](assets/images/articles/certificates-without-the-jargon.webp){ class="catalogue-logo" }

    A plain-language guide to X.509 certificates for developers — keys,
    CSRs, self-signed vs CA-signed, trust stores, and what actually matters
    when generating certs for tools and tests.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Tools</span>

-   **[CLI Design](articles/cli-design.md)**

    ---

    ![Article](assets/images/articles/cli-design.webp){ class="catalogue-logo" }

    Practical CLI design for open-source tools — flags and arguments, exit
    codes, stdout versus stderr, helpful errors, and interfaces that feel
    good in scripts and human hands.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Tools</span>

-   **[Coding Standards](articles/coding-standards.md)**

    ---

    ![Article](assets/images/articles/coding-standards.webp){ class="catalogue-logo" }

    Explore the importance of coding standards for consistent, maintainable
    code and discover how automation can simplify enforcement, ensuring
    quality in software development.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Standards</span>

-   **[Config Design](articles/config-design.md)**

    ---

    ![Article](assets/images/articles/config-design.webp){ class="catalogue-logo" }

    Practical configuration design for tools — flags, environment variables,
    files, precedence, secrets, and defaults that stay understandable as
    projects grow.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Tools</span>

-   **[Containers for CLI Tools](articles/containers-for-cli-tools.md)**

    ---

    ![Article](assets/images/articles/containers-for-cli-tools.webp){ class="catalogue-logo" }

    When and how to ship CLI tools as containers — pinning base images, non-
    root users, small attack surface, and avoiding container anti-patterns
    for simple utilities.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Tools</span>

-   **[Contributing Without the Drama](articles/contributing-without-the-drama.md)**

    ---

    ![Article](assets/images/articles/contributing-without-the-drama.webp){ class="catalogue-logo" }

    Practical guidance for opening useful issues and pull requests in open-
    source projects — small diffs, clear context, good first issues, and
    knowing when not to bikeshed.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Community</span>

-   **[Cybersecurity & Chess](articles/cybersecurity-and-chess.md)**

    ---

    ![Article](assets/images/articles/cybersecurity-and-chess.webp){ class="catalogue-logo" }

    Discover the strategic parallels between cybersecurity and chess, where
    anticipation, adaptation, and calculated risks define success in both
    digital and game-based battlefields.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Strategy</span>

-   **[Dependency Hygiene](articles/dependency-hygiene.md)**

    ---

    ![Article](assets/images/articles/dependency-hygiene.webp){ class="catalogue-logo" }

    Practical dependency hygiene for open-source and small teams — pinning,
    lockfiles, audits, supply-chain basics, and keeping your software supply
    line trustworthy without enterprise ceremony.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Deprecation Without Chaos](articles/deprecation-without-chaos.md)**

    ---

    ![Article](assets/images/articles/deprecation-without-chaos.webp){ class="catalogue-logo" }

    How to deprecate APIs and flags calmly — warnings, timelines, SemVer,
    migration paths, and removing old behaviour without surprising your
    users.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Engineering</span>

-   **[Docs That Don't Rot](articles/docs-that-dont-rot.md)**

    ---

    ![Article](assets/images/articles/docs-that-dont-rot.webp){ class="catalogue-logo" }

    How to keep project documentation alive — examples as tests, docs sites
    that ship with releases, screenshots that stay honest, and habits that
    stop docs from quietly lying.

    <span class="catalogue-category">Documentation</span>
    <span class="catalogue-category">Open Source</span>

-   **[Encryption at Rest for Repos](articles/encryption-at-rest-for-repos.md)**

    ---

    ![Article](assets/images/articles/encryption-at-rest-for-repos.webp){ class="catalogue-logo" }

    Practical guidance for encrypting secrets in Git repositories — when
    git-crypt and similar tools help, key management pitfalls, and safer
    patterns for small teams.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Git</span>

-   **[Error Handling People Can Use](articles/error-handling-people-can-use.md)**

    ---

    ![Article](assets/images/articles/error-handling-people-can-use.webp){ class="catalogue-logo" }

    Practical error handling for CLIs and libraries — clear messages, exit
    codes, retries, typed failures, and when to crash versus recover.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Tools</span>

-   **[Git Workflows for Tiny Teams](articles/git-workflows-for-tiny-teams.md)**

    ---

    ![Article](assets/images/articles/git-workflows-for-tiny-teams.webp){ class="catalogue-logo" }

    Practical Git workflows for small teams and solo maintainers — trunk-
    based development, short-lived branches, pull requests, and release tags
    without enterprise branching theatre.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Process</span>

-   **[GitHub Actions](articles/github-actions.md)**

    ---

    ![Article](assets/images/articles/github-actions.webp){ class="catalogue-logo" }

    Learn how to use GitHub Actions for CI/CD, with a step-by-step guide on
    automating builds, tests, and deployments, complete with YAML
    configurations and best practices.

    <span class="catalogue-category">CI/CD</span>
    <span class="catalogue-category">GitHub</span>

-   **[Input Validation That Sticks](articles/input-validation-that-sticks.md)**

    ---

    ![Article](assets/images/articles/input-validation-that-sticks.webp){ class="catalogue-logo" }

    Practical input validation for CLIs and small services — paths, URLs,
    commands, sizes, and the failure modes that turn tools into exploit
    gadgets.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Key Lifecycle](articles/key-lifecycle.md)**

    ---

    ![Article](assets/images/articles/key-lifecycle.webp){ class="catalogue-logo" }

    Practical key lifecycle for small security tools — generate, distribute,
    rotate, revoke, and retire cryptographic keys and certificates without
    drama.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Least Privilege for CI](articles/least-privilege-for-ci.md)**

    ---

    ![Article](assets/images/articles/least-privilege-for-ci.webp){ class="catalogue-logo" }

    Hardening CI/CD credentials — short-lived tokens, OIDC, protected
    environments, and GitHub Actions patterns that avoid long-lived secrets
    in pipelines.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">CI/CD</span>

-   **[Licenses for Humans](articles/licenses-for-humans.md)**

    ---

    ![Article](assets/images/articles/licenses-for-humans.webp){ class="catalogue-logo" }

    A plain-language guide to common open-source licenses for people
    publishing tools — MIT, Apache-2.0, GPL family trade-offs, why LICENSE
    files matter, and how to choose without a law degree.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Community</span>

-   **[Maintainer Boundaries](articles/maintainer-boundaries.md)**

    ---

    ![Article](assets/images/articles/maintainer-boundaries.webp){ class="catalogue-logo" }

    Healthy boundaries for open-source maintainers — saying no, defining
    scope, managing expectations, and protecting energy without abandoning
    the project.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Community</span>

-   **[mTLS and Client Certificates](articles/mtls-and-client-certificates.md)**

    ---

    ![Article](assets/images/articles/mtls-and-client-certificates.webp){ class="catalogue-logo" }

    A practical introduction to mutual TLS and client certificates — how
    they differ from ordinary HTTPS, when they help, and how small tools
    should issue and verify them.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Certificates</span>

-   **[Observability for Small Projects](articles/observability-for-small-projects.md)**

    ---

    ![Article](assets/images/articles/observability-for-small-projects.webp){ class="catalogue-logo" }

    Practical observability for CLIs, libraries, and small services — useful
    logs, health signals, failure modes, and knowing what broke without
    needing an enterprise APM stack.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">DevOps</span>

-   **[Programming Fundamentals](articles/programming-fundamentals.md)**

    ---

    ![Article](assets/images/articles/programming-fundamentals.webp){ class="catalogue-logo" }

    Discover why mastering programming principles and fundamentals is more
    valuable than focusing on a specific language, enabling you to adapt,
    debug, and collaborate more effectively in an evolving tech landscape.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Fundamentals</span>

-   **[README as Product](articles/readme-as-product.md)**

    ---

    ![Article](assets/images/articles/readme-as-product.webp){ class="catalogue-logo" }

    Treat your README as the product surface of an open-source project —
    clear install steps, honest examples, trustworthy badges, and a path
    from curiosity to first success.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Documentation</span>

-   **[Red Team vs Blue Team](articles/red-team-vs-blue-team.md)**

    ---

    ![Article](assets/images/articles/red-team-vs-blue-team.webp){ class="catalogue-logo" }

    Learn the differences between Red Teams and Blue Teams in cybersecurity,
    their roles in attack and defence simulations, and how they work
    together to strengthen an organization's security posture.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Ops</span>

-   **[Release Automation](articles/release-automation.md)**

    ---

    ![Article](assets/images/articles/release-automation.webp){ class="catalogue-logo" }

    How to automate releases for open-source projects — tags, changelogs,
    GitHub Releases, package publishing, and CI checks that make shipping
    routine instead of heroic.

    <span class="catalogue-category">CI/CD</span>
    <span class="catalogue-category">Open Source</span>

-   **[Reproducible Builds](articles/reproducible-builds.md)**

    ---

    ![Article](assets/images/articles/reproducible-builds.webp){ class="catalogue-logo" }

    Lightweight reproducible builds for small tools — pinning inputs, stable
    artefacts, and practical steps toward bit-for-bit or practically
    identical releases without enterprise ceremony.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Responsible Dependency Updates](articles/responsible-dependency-updates.md)**

    ---

    ![Article](assets/images/articles/responsible-dependency-updates.webp){ class="catalogue-logo" }

    A practical cadence for dependency updates — Dependabot-style PRs,
    ignore rules, reading majors, and keeping upgrades boring without
    ignoring security fixes.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Right Tools for the Job](articles/right-tools-for-the-job.md)**

    ---

    ![Article](assets/images/articles/right-tools-for-the-job.webp){ class="catalogue-logo" }

    Learn why choosing the right tools for the job is crucial in software
    development. Discover how to select the best programming languages,
    operating systems, cloud providers, frameworks, and databases based on
    specific project requirements.

    <span class="catalogue-category">Tools</span>
    <span class="catalogue-category">Engineering</span>

-   **[SAST and DAST](articles/sast-and-dast.md)**

    ---

    ![Article](assets/images/articles/sast-and-dast.webp){ class="catalogue-logo" }

    Learn about Static Application Security Testing (SAST) and Dynamic
    Application Security Testing (DAST) in software development. Understand
    how these tools help identify and mitigate vulnerabilities, improve
    security, and ensure regulatory compliance.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Secrets Management](articles/secrets-management.md)**

    ---

    ![Article](assets/images/articles/secrets-management.webp){ class="catalogue-logo" }

    Learn the essentials of secrets management, its importance in protecting
    sensitive data, best practices for secure handling, and an overview of
    tools to safeguard your organization's credentials.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">DevOps</span>

-   **[Secure Defaults](articles/secure-defaults.md)**

    ---

    ![Article](assets/images/articles/secure-defaults.webp){ class="catalogue-logo" }

    Designing secure defaults for tools and libraries — fail closed, least
    privilege, dangerous features opt-in, and interfaces that make the safe
    path the easy path.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Design</span>

-   **[Secure Logging](articles/secure-logging.md)**

    ---

    ![Article](assets/images/articles/secure-logging.webp){ class="catalogue-logo" }

    Practical secure logging for tools and services — what never to log,
    redaction, crash reports, debug flags, and keeping observability from
    becoming a leak.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Security by Design](articles/security-by-design.md)**

    ---

    ![Article](assets/images/articles/security-by-design.webp){ class="catalogue-logo" }

    Explore the concept of Security by Design, its importance in building
    resilient systems, and how to apply its principles across software
    development, infrastructure, and cloud environments for proactive
    cybersecurity.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Design</span>

-   **[Security Disclosures That Work](articles/security-disclosures-that-work.md)**

    ---

    ![Article](assets/images/articles/security-disclosures-that-work.webp){ class="catalogue-logo" }

    Practical security disclosure for small open-source projects —
    SECURITY.md, private reporting, triage, credit, and promises maintainers
    can actually keep.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Open Source</span>

-   **[Semantic Versioning](articles/semantic-versioning.md)**

    ---

    ![Article](assets/images/articles/semantic-versioning.webp){ class="catalogue-logo" }

    A practical guide to semantic versioning for open-source tools — major,
    minor, and patch releases, 0.x realities, deprecations, and
    communicating breaking changes without surprising your users.

    <span class="catalogue-category">Open Source</span>
    <span class="catalogue-category">Engineering</span>

-   **[Supply-Chain Signing](articles/supply-chain-signing.md)**

    ---

    ![Article](assets/images/articles/supply-chain-signing.webp){ class="catalogue-logo" }

    Practical supply-chain signing for open-source releases — checksums,
    signatures, provenance, and verification steps users can actually
    follow.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Open Source</span>

-   **[Testing What Matters](articles/testing-what-matters.md)**

    ---

    ![Article](assets/images/articles/testing-what-matters.webp){ class="catalogue-logo" }

    Why high coverage can be a vanity metric, how to test behaviour instead
    of mocks, and how small open-source projects can build a test suite that
    catches real regressions without drowning contributors.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Testing</span>

-   **[The Cybersecurity Rainbow](articles/the-cybersecurity-rainbow.md)**

    ---

    ![Article](assets/images/articles/the-cybersecurity-rainbow.webp){ class="catalogue-logo" }

    Explore the roles of the color-coded cybersecurity teams—Red, Blue,
    Purple, Green, Yellow, Orange, and White—and learn how they contribute
    to a comprehensive, resilient cybersecurity strategy.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Ops</span>

-   **[The Optimisation Trap](articles/the-optimization-trap.md)**

    ---

    ![Article](assets/images/articles/the-optimization-trap.webp){ class="catalogue-logo" }

    Discover how to avoid the optimisation trap in software engineering.
    Learn why it's essential to focus on purpose-driven improvements,
    inspired by Elon Musk's insights on building the right things, not just
    better things.

    <span class="catalogue-category">Engineering</span>
    <span class="catalogue-category">Mindset</span>

-   **[Threat Modelling for Small Tools](articles/threat-modelling-for-small-tools.md)**

    ---

    ![Article](assets/images/articles/threat-modelling-for-small-tools.webp){ class="catalogue-logo" }

    Lightweight threat modelling for CLIs, libraries, and small services —
    assets, attackers, trust boundaries, and a practical checklist without
    enterprise ceremony.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Engineering</span>

-   **[Understanding CI/CD](articles/understanding-ci-cd.md)**

    ---

    ![Article](assets/images/articles/understanding-ci-cd.webp){ class="catalogue-logo" }

    Explore the fundamentals of CI/CD in software development. Understand
    the benefits, challenges, and best practices to implement Continuous
    Integration and Continuous Delivery/Deployment effectively.

    <span class="catalogue-category">CI/CD</span>
    <span class="catalogue-category">DevOps</span>

-   **[Writing a SECURITY.md That People Use](articles/writing-a-security-md-that-people-use.md)**

    ---

    ![Article](assets/images/articles/writing-a-security-md-that-people-use.webp){ class="catalogue-logo" }

    A practical SECURITY.md playbook for small projects — what to include,
    example structure, scope statements, and making the security policy easy
    to find and follow.

    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Open Source</span>

</div>

<div class="catalogue-empty-state" data-article-empty hidden markdown>

:material-magnify: No articles match the current filters.

Try clearing the search or choosing a different tag.

</div>
