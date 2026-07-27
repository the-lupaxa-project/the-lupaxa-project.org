---
hide:
  - navigation
  - toc
---

<div class="filter-panel" data-project-filters>
    <div class="filter-panel-search">
        <label for="project-search">Search projects</label>
        <input id="project-search" type="search" placeholder="Search by project name, description, or category..." autocomplete="off" data-project-search/>
    </div>
    <div class="filter-panel-select">
        <label for="project-organisation">Organisation</label>
        <select id="project-organisation" data-project-organisation>
            <option value="">All organisations</option>
        </select>
    </div>
    <div class="filter-panel-select">
        <label for="project-category">Category</label>
        <select id="project-category" data-project-category>
            <option value="">All categories</option>
        </select>
    </div>
    <div class="filter-panel-actions">
        <button type="button" class="filter-panel-clear" data-project-clear>Clear filters</button>
    </div>
    <div class="filter-panel-summary" aria-live="polite" data-project-summary>Showing all projects</div>
</div>

<div class="grid cards catalogue-grid" data-project-catalogue markdown>

-   :material-source-repository:{ .lg .middle } **Certificate Tool**

    ---

    <img
        class="catalogue-logo"
        data-organisation="Security Toolbox"
        src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/security-toolbox/readme-logo-128.png"
        alt="Security Toolbox"
    />

    Generate self-signed X.509 certificates, certificate signing requests (CSRs), and private keys using a modern, fully typed Python command-line application and library.

    Designed for automation as well as interactive use, it provides a clean and consistent interface for creating development and testing certificates.

    <span class="catalogue-category">Certificates</span>
    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Python</span>

    ---

    <a
        class="catalogue-action catalogue-action--repository"
        href="https://github.com/lupaxa-security-toolbox/certtool"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-github:</span>
        View on GitHub
    </a>
    <a
        class="catalogue-action catalogue-action--documentation"
        href="https://lupaxa-security-toolbox.github.io/certtool/"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-book-open-page-variant:</span>
        Documentation
    </a>

-   :material-source-repository:{ .lg .middle } **Git Crypt Manager**

    ---

    <img
        class="catalogue-logo"
        data-organisation="Security Toolbox"
        src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/security-toolbox/readme-logo-128.png"
        alt="Security Toolbox"
    />

    Simplify the management of encrypted Git repositories with a guided automation tool built around [git-crypt](https://github.com/AGWA/git-crypt).

    The project helps initialise, configure, and maintain encrypted repositories while reducing the complexity of day-to-day key management.

    <span class="catalogue-category">Encryption</span>
    <span class="catalogue-category">Security</span>
    <span class="catalogue-category">Git</span>
    <span class="catalogue-category">Bash</span>

    ---

    <a
        class="catalogue-action catalogue-action--repository"
        href="https://github.com/lupaxa-security-toolbox/git-crypt-manager"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-github:</span>
        View on GitHub
    </a>
    <a
        class="catalogue-action catalogue-action--documentation"
        href="https://lupaxa-security-toolbox.github.io/git-crypt-manager/"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-book-open-page-variant:</span>
        Documentation
    </a>

-   :material-source-repository:{ .lg .middle } **GitHub Repository Sync**

    ---

    <img
        class="catalogue-logo"
        data-organisation="The Lupaxa Internal Toolbox"
        src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/the-lupaxa-internal-toolbox/readme-logo-128.png"
        alt="Lupaxa Internal Toolbox"
    />

    Clone, organise, and safely synchronise large collections of GitHub repositories using a declarative JSON5 configuration file.

    Each repository is inspected before any Git operation is performed, ensuring that only repositories confirmed to be in a safe state are automatically updated.

    <span class="catalogue-category">GitHub</span>
    <span class="catalogue-category">Automation</span>
    <span class="catalogue-category">Repository Management</span>
    <span class="catalogue-category">Python</span>

    ---

    <a
        class="catalogue-action catalogue-action--repository"
        href="https://github.com/the-lupaxa-internal-toolbox/github-repo-sync"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-github:</span>
        View on GitHub
    </a>
    <a
        class="catalogue-action catalogue-action--documentation"
        href="https://github-repo-sync.thelupaxaproject.org/"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-book-open-page-variant:</span>
        Documentation
    </a>

-   :material-source-repository:{ .lg .middle } **Shared Reusable Workflows**

    ---

    <img
        class="catalogue-logo"
        data-organisation="The Lupaxa Project"
        src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/the-lupaxa-project/readme-logo-128.png"
        alt="The Lupaxa Project"
    />

    A collection of reusable GitHub Actions workflows for repository quality, continuous integration, documentation, security, and automation.

    Designed to provide consistent workflows across The Lupaxa Project, these reusable components reduce duplication and simplify repository management.

    <span class="catalogue-category">GitHub Actions</span>
    <span class="catalogue-category">Automation</span>
    <span class="catalogue-category">Continuous Integration</span>

    ---

    <a
        class="catalogue-action catalogue-action--repository"
        href="https://github.com/the-lupaxa-project/workflows"
        target="_blank"
        rel="noopener noreferrer">
        <span class="md-icon">:material-github:</span>
        View on GitHub
    </a>

</div>

<div class="catalogue-empty-state" data-project-empty hidden markdown>

:material-filter-off:{ .lg }

**No matching projects**

Try changing the search text or selecting different filters.

</div>
