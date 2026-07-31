"""Helpers for article front matter and the articles index page."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import yaml

# Optional shorter titles for cards / pager (page H1 can stay longer).
ARTICLE_CARD_TITLES: dict[str, str] = {}

ARTICLE_TAGS: dict[str, list[str]] = {
    "certificates-without-the-jargon": ["Security", "Tools"],
    "cli-design": ["Engineering", "Tools"],
    "coding-standards": ["Engineering", "Standards"],
    "config-design": ["Engineering", "Tools"],
    "containers-for-cli-tools": ["Security", "Tools"],
    "contributing-without-the-drama": ["Open Source", "Community"],
    "cybersecurity-and-chess": ["Security", "Strategy"],
    "dependency-hygiene": ["Security", "Engineering"],
    "deprecation-without-chaos": ["Open Source", "Engineering"],
    "docs-that-dont-rot": ["Documentation", "Open Source"],
    "encryption-at-rest-for-repos": ["Security", "Git"],
    "error-handling-people-can-use": ["Engineering", "Tools"],
    "git-workflows-for-tiny-teams": ["Engineering", "Process"],
    "github-actions": ["CI/CD", "GitHub"],
    "input-validation-that-sticks": ["Security", "Engineering"],
    "key-lifecycle": ["Security", "Engineering"],
    "least-privilege-for-ci": ["Security", "CI/CD"],
    "licenses-for-humans": ["Open Source", "Community"],
    "maintainer-boundaries": ["Open Source", "Community"],
    "mtls-and-client-certificates": ["Security", "Certificates"],
    "observability-for-small-projects": ["Engineering", "DevOps"],
    "programming-fundamentals": ["Engineering", "Fundamentals"],
    "readme-as-product": ["Open Source", "Documentation"],
    "red-team-vs-blue-team": ["Security", "Ops"],
    "release-automation": ["CI/CD", "Open Source"],
    "reproducible-builds": ["Security", "Engineering"],
    "responsible-dependency-updates": ["Security", "Engineering"],
    "right-tools-for-the-job": ["Tools", "Engineering"],
    "sast-and-dast": ["Security", "Engineering"],
    "secrets-management": ["Security", "DevOps"],
    "secure-defaults": ["Security", "Design"],
    "secure-logging": ["Security", "Engineering"],
    "security-by-design": ["Security", "Design"],
    "security-disclosures-that-work": ["Security", "Open Source"],
    "semantic-versioning": ["Open Source", "Engineering"],
    "supply-chain-signing": ["Security", "Open Source"],
    "testing-what-matters": ["Engineering", "Testing"],
    "the-cybersecurity-rainbow": ["Security", "Ops"],
    "the-optimization-trap": ["Engineering", "Mindset"],
    "threat-modelling-for-small-tools": ["Security", "Engineering"],
    "understanding-ci-cd": ["CI/CD", "DevOps"],
    "writing-a-security-md-that-people-use": ["Security", "Open Source"],
}


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Return (meta, body) for a Markdown document with optional YAML front matter."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    meta = yaml.safe_load(raw) or {}
    if not isinstance(meta, dict):
        return {}, text
    return meta, body


def is_published(meta: dict[str, Any]) -> bool:
    """Articles are published unless explicitly set to false."""
    return bool(meta.get("published", True))


def load_article_meta(path: Path) -> dict[str, Any]:
    return split_front_matter(path.read_text(encoding="utf-8"))[0]


def display_title(slug: str, meta: dict[str, Any]) -> str:
    if slug in ARTICLE_CARD_TITLES:
        return ARTICLE_CARD_TITLES[slug]
    title = meta.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return slug.replace("-", " ").title()


def article_tags(slug: str, meta: dict[str, Any]) -> list[str]:
    tags = meta.get("tags")
    if isinstance(tags, list) and tags:
        return [str(tag) for tag in tags]
    return list(ARTICLE_TAGS.get(slug, ["Engineering"]))


def format_front_matter(
    *,
    title: str,
    published: bool = True,
    description: str = "",
    tags: list[str] | None = None,
) -> str:
    payload: dict[str, Any] = {
        "title": title,
        "published": published,
        "hide": ["navigation", "toc"],
    }
    if description:
        payload["description"] = description
    if tags:
        payload["tags"] = tags
    dumped = yaml.safe_dump(
        payload,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    ).strip()
    return f"---\n{dumped}\n---\n\n"


def _article_entry(slug: str, meta: dict[str, Any]) -> str:
    title = display_title(slug, meta)
    desc = str(meta.get("description") or "").strip()
    tags = article_tags(slug, meta)
    desc_lines = textwrap.wrap(desc, width=72) or [""]
    desc_block = "\n    ".join(desc_lines)
    tag_spans = "\n    ".join(
        f'<span class="catalogue-category">{tag}</span>' for tag in tags
    )
    return (
        f"-   **[{title}](articles/{slug}.md)**\n"
        f"\n"
        f"    ---\n"
        f"\n"
        f'    ![Article](assets/images/articles/{slug}.webp){{ class="catalogue-logo" }}\n'
        f"\n"
        f"    {desc_block}\n"
        f"\n"
        f"    {tag_spans}\n"
    )


def rebuild_articles_index(docs_dir: Path) -> int:
    """Rewrite articles.md from published article front matter. Returns count."""
    articles_dir = docs_dir / "articles"
    index_path = docs_dir / "articles.md"
    items: list[tuple[str, dict[str, Any]]] = []

    for path in sorted(articles_dir.glob("*.md")):
        meta = load_article_meta(path)
        if not is_published(meta):
            continue
        items.append((path.stem, meta))

    items.sort(key=lambda item: display_title(item[0], item[1]).casefold())
    entries = "\n".join(_article_entry(slug, meta) for slug, meta in items)

    header = textwrap.dedent(
        """\
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
              <option value="">All Tags</option>
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

        """
    )
    footer = textwrap.dedent(
        """
        </div>

        <div class="catalogue-empty-state" data-article-empty hidden markdown>

        :material-magnify: No articles match the current filters.

        Try clearing the search or choosing a different tag.

        </div>
        """
    )
    # Only write when content changes — unconditional writes retrigger
    # `mkdocs serve` watch and cause a rebuild loop.
    content = header + entries + footer
    if index_path.exists() and index_path.read_text(encoding="utf-8") == content:
        return len(items)

    index_path.write_text(content, encoding="utf-8")
    return len(items)
