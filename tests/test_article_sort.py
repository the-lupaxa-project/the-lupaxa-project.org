from articles_lib import _article_entry, rebuild_articles_index


def test_article_entry_includes_publish_date_on_logo():
    entry = _article_entry(
        "example",
        {
            "title": "Example Article",
            "description": "Desc",
            "publish_date": "2026-07-31",
            "tags": ["Security"],
        },
    )
    assert 'data-publish-date="2026-07-31"' in entry
    assert "catalogue-logo" in entry


def test_article_entry_omits_publish_date_when_missing():
    entry = _article_entry(
        "example",
        {"title": "Example Article", "description": "Desc", "tags": ["Security"]},
    )
    assert "data-publish-date" not in entry


def test_articles_index_includes_sort_toggle(tmp_path):
    articles = tmp_path / "articles"
    articles.mkdir()
    (articles / "alpha.md").write_text(
        "---\ntitle: Alpha\npublished: true\npublish_date: '2026-01-01'\n"
        "description: A\ntags: [Engineering]\n---\n\n# Alpha\n",
        encoding="utf-8",
    )
    rebuild_articles_index(tmp_path)
    html = (tmp_path / "articles.md").read_text(encoding="utf-8")
    assert 'class="filter-panel filter-panel--with-sort"' in html
    assert "filter-panel--compact" not in html
    assert "filter-panel-toolbar" in html
    assert "data-filter-expand" in html
    assert "filter-panel-expand__icon" in html
    assert "data-article-summary" in html
    assert '<label id="article-status-label">View Articles</label>' in html
    assert 'data-article-status="all"' in html
    assert 'data-article-status="new"' in html
    assert 'id="article-category"' in html  # Tag remains a select
    assert 'id="article-status"' not in html  # Status is a toggle, not a select
    assert '<label id="article-sort-label">Sort</label>' in html
    assert 'data-article-sort="alpha"' in html
    assert 'data-article-sort="newest"' in html
    assert "A–Z" in html
    assert "Newest" in html
    assert 'data-publish-date="2026-01-01"' in html
    assert "filter-panel-toggle__options" in html
    # Toolbar (Filters + summary), then search | tag | status | sort | clear
    assert html.index("filter-panel-toolbar") < html.index("data-article-summary")
    assert html.index("data-article-summary") < html.index("filter-panel-search")
    assert html.index("article-status-label") < html.index("article-sort-label")
    assert html.index("article-sort-label") < html.index("filter-panel-actions")
