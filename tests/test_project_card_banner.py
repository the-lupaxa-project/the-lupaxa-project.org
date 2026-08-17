import re
from datetime import date, timedelta
from pathlib import Path

import yaml

import main

ROOT = Path(__file__).resolve().parent.parent


class _FakeEnv:
    """Minimal stand-in for the mkdocs-macros environment used by define_env."""

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = str(project_dir)
        self.variables: dict = {}
        self.macros: dict = {}

    def macro(self, func):
        self.macros[func.__name__] = func
        return func


def _write_yaml(path: Path, data) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _synthetic_project(**overrides) -> dict:
    project = {
        "id": "synthetic-project",
        "published": True,
        "name": "Synthetic Project",
        "icon": "material-source-repository",
        "publish_date": "2025-01-01",
        "description": "A synthetic project used for testing.",
        "categories": ["Testing"],
        "organisation": "Test Org",
        "logo": "https://example.com/logo.png",
        "repository": "https://github.com/example/synthetic",
    }
    project.update(overrides)
    return project


def _catalogue_grid(tmp_path: Path, monkeypatch, projects: list[dict]):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_yaml(data_dir / "organisations.yml", [])
    _write_yaml(data_dir / "policies.yml", [])
    _write_yaml(data_dir / "projects.yml", projects)

    monkeypatch.setattr(main, "DATA_DIR", data_dir)

    env = _FakeEnv(ROOT)
    main.define_env(env)
    return env.macros["catalogue_grid"]


def test_project_card_rejects_article_only_presets(tmp_path, monkeypatch):
    """Project cards must not render banners from the article-only preset set."""
    projects = [_synthetic_project(banner="new")]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" not in markup
    assert "New Article" not in markup


def test_project_card_shows_fresh_released_banner(tmp_path, monkeypatch):
    fresh_date = (date.today() - timedelta(days=1)).isoformat()
    projects = [_synthetic_project(banner="released", released_date=fresh_date)]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" in markup
    assert "Released" in markup
    assert "v0.1.0" in markup


def test_project_card_hides_expired_released_banner(tmp_path, monkeypatch):
    expired_date = (date.today() - timedelta(days=400)).isoformat()
    projects = [_synthetic_project(banner="released", released_date=expired_date)]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" not in markup


def test_project_card_hides_released_banner_without_released_date(tmp_path, monkeypatch):
    projects = [_synthetic_project(banner="released")]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" not in markup


def test_project_card_shows_non_time_limited_preset(tmp_path, monkeypatch):
    projects = [_synthetic_project(banner="in-development")]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" in markup
    assert "In Development" in markup
    assert "v0.1.0" in markup


def test_project_card_released_keeps_status_and_shows_version(tmp_path, monkeypatch):
    fresh_date = (date.today() - timedelta(days=1)).isoformat()
    projects = [
        _synthetic_project(
            banner="released",
            released_date=fresh_date,
            version="0.1.0",
        )
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "Released" in markup
    assert "v0.1.0" in markup
    assert 'data-banner-status="released"' in markup
    assert "catalogue-banner--blue" in markup


def test_project_card_later_version_stays_released(tmp_path, monkeypatch):
    fresh_date = (date.today() - timedelta(days=1)).isoformat()
    projects = [
        _synthetic_project(
            banner="released",
            released_date=fresh_date,
            version="1.2.0",
        )
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "Released" in markup
    assert "v1.2.0" in markup
    assert 'data-banner-status="released"' in markup
    assert "catalogue-banner--blue" in markup


def test_project_card_in_testing_keeps_status_and_shows_version(tmp_path, monkeypatch):
    projects = [_synthetic_project(banner="in-testing", version="1.2.0")]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "In Testing" in markup
    assert "v1.2.0" in markup
    assert 'data-banner-status="in-testing"' in markup


def test_catalogue_grid_projects_emit_in_name_order(tmp_path, monkeypatch):
    projects = [
        _synthetic_project(id="ccc", name="CCC"),
        _synthetic_project(id="action-lint", name="Action Lint"),
        _synthetic_project(id="aaa", name="AAA"),
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")
    names = re.findall(r'data-name="([^"]+)"', markup)

    assert names == ["AAA", "Action Lint", "CCC"]


def test_project_card_local_logo_is_site_root_relative(tmp_path, monkeypatch):
    """Raw HTML img src must work from /projects/, not only the homepage."""
    projects = [
        _synthetic_project(logo="assets/images/brand/organisation-cicd-toolbox-logo.png")
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert 'src="/assets/images/brand/organisation-cicd-toolbox-logo.png"' in markup


def test_project_card_keeps_remote_logo_url(tmp_path, monkeypatch):
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, [_synthetic_project()])

    markup = catalogue_grid("project", "project")

    assert 'src="https://example.com/logo.png"' in markup


def test_project_card_includes_publish_date_on_logo(tmp_path, monkeypatch):
    projects = [_synthetic_project(publish_date="2026-08-01")]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert 'data-publish-date="2026-08-01"' in markup
    assert 'data-name="Synthetic Project"' in markup
    assert "catalogue-logo" in markup
    assert "data-released-date" not in markup


def test_project_card_includes_released_date_time_on_logo(tmp_path, monkeypatch):
    projects = [
        _synthetic_project(
            publish_date="2026-08-01T09:00:00",
            released_date="2026-08-17T14:00:00",
        )
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert 'data-publish-date="2026-08-01T09:00:00"' in markup
    assert 'data-released-date="2026-08-17T14:00:00"' in markup
