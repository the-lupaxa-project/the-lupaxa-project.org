"""Helpers for article front matter and the articles index page."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Any

import yaml

# Optional shorter titles for cards / pager (page H1 can stay longer).
ARTICLE_CARD_TITLES: dict[str, str] = {
    "ai-and-ml": "AI & Machine Learning",
}

ARTICLE_TAGS: dict[str, list[str]] = {
    "agile-vs-waterfall": ["Agile", "Process"],
    "ai-and-ml": ["AI", "ML"],
    "aptitude-and-attitude": ["Career", "Mindset"],
    "coding-standards": ["Engineering", "Standards"],
    "cybersecurity-and-chess": ["Security", "Strategy"],
    "developers-and-ai": ["AI", "Development"],
    "dont-fear-failure": ["Mindset", "Growth"],
    "feature-flags": ["Engineering", "Delivery"],
    "github-actions": ["CI/CD", "GitHub"],
    "high-and-low-level-design": ["Architecture", "Design"],
    "infrastructure-as-code": ["DevOps", "IaC"],
    "leaders-vs-managers": ["Leadership", "Career"],
    "monoliths-vs-microservices": ["Architecture", "Systems"],
    "never-stop-learning": ["Career", "Learning"],
    "programmers-vs-software-engineers": ["Career", "Engineering"],
    "programming-fundamentals": ["Engineering", "Fundamentals"],
    "python-the-swiss-army-knife": ["Python", "Tools"],
    "red-team-vs-blue-team": ["Security", "Ops"],
    "secrets-management": ["Security", "DevOps"],
    "security-by-design": ["Security", "Design"],
    "software-automation": ["Automation", "DevOps"],
    "software-development-life-cycle": ["Process", "SDLC"],
    "software-security": ["Security", "Engineering"],
    "the-cybersecurity-rainbow": ["Security", "Ops"],
    "the-optimization-trap": ["Engineering", "Mindset"],
    "the-role-of-software-architects": ["Architecture", "Career"],
    "tools-for-jobs": ["Tools", "Engineering"],
    "understanding-ci-cd": ["CI/CD", "DevOps"],
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
        f'    ![Article](assets/images/articles/{slug}.png){{ class="catalogue-logo" }}\n'
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
