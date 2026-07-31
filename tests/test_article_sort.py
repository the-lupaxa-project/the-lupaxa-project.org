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
    assert 'class="filter-panel-sort"' in html
    assert 'data-article-sort="alpha"' in html
    assert 'data-article-sort="newest"' in html
    assert "A–Z" in html
    assert "Newest" in html
    assert 'data-publish-date="2026-01-01"' in html
