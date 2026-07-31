from pathlib import Path

import yaml

from articles_lib import is_published, load_article_meta
from banner_lib import parse_iso_date

ROOT = Path(__file__).resolve().parent.parent


def test_all_projects_have_parseable_publish_date():
    projects_path = ROOT / "data" / "projects.yml"
    projects = yaml.safe_load(projects_path.read_text(encoding="utf-8")) or []
    assert projects, "expected at least one project in data/projects.yml"

    for project in projects:
        publish_date = project.get("publish_date")
        identifier = project.get("id", "<unknown>")
        assert publish_date is not None, f"project {identifier!r} is missing publish_date"
        assert parse_iso_date(publish_date) is not None, (
            f"project {identifier!r} has unparseable publish_date: {publish_date!r}"
        )


def test_all_published_articles_have_parseable_publish_date():
    articles_dir = ROOT / "mkdocs" / "articles"
    checked = 0

    for path in sorted(articles_dir.glob("*.md")):
        meta = load_article_meta(path)
        if not is_published(meta):
            continue
        checked += 1
        publish_date = meta.get("publish_date")
        assert publish_date is not None, f"article {path.name!r} is missing publish_date"
        assert parse_iso_date(publish_date) is not None, (
            f"article {path.name!r} has unparseable publish_date: {publish_date!r}"
        )

    assert checked > 0, "expected at least one published article"
