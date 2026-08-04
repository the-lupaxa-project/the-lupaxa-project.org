"""Newest projects home selection and macro."""

from pathlib import Path

import main

ROOT = Path(__file__).resolve().parent.parent


def _project(identifier: str, publish_date: str, **extra):
    return {
        "id": identifier,
        "name": identifier.replace("-", " ").title(),
        "published": True,
        "publish_date": publish_date,
        "description": "Test project.",
        "categories": ["Test"],
        "organisation": "Git Toolbox",
        "logo": "https://example.com/logo.png",
        "logo_alt": "Test",
        "repository": f"https://github.com/example/{identifier}",
        **extra,
    }


def test_select_newest_projects_orders_by_publish_date_then_id():
    projects = [
        _project("older", "2026-01-01"),
        _project("mid-b", "2026-06-01"),
        _project("mid-a", "2026-06-01"),
        _project("newest", "2026-08-04"),
        _project("also-new", "2026-08-03"),
        _project("third", "2026-07-01"),
        _project("fourth", "2026-05-01"),
    ]

    selected = main.select_newest_projects(projects, limit=6)
    assert [item["id"] for item in selected] == [
        "newest",
        "also-new",
        "third",
        "mid-a",
        "mid-b",
        "fourth",
    ]


def test_select_newest_projects_respects_limit():
    projects = [_project(f"p{i}", f"2026-01-{i:02d}") for i in range(1, 10)]
    assert len(main.select_newest_projects(projects, limit=6)) == 6
    assert main.NEWEST_PROJECTS_LIMIT == 6


def test_select_newest_projects_skips_unparseable_dates_last():
    projects = [
        _project("dated", "2026-08-01"),
        _project("bad-date", "not-a-date"),
    ]
    selected = main.select_newest_projects(projects, limit=6)
    assert [item["id"] for item in selected] == ["dated", "bad-date"]
