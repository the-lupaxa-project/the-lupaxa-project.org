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
    projects = [
        _synthetic_project(banner="released", released_date=fresh_date)
    ]
    catalogue_grid = _catalogue_grid(tmp_path, monkeypatch, projects)

    markup = catalogue_grid("project", "project")

    assert "catalogue-banner" in markup
    assert "Released" in markup


def test_project_card_hides_expired_released_banner(tmp_path, monkeypatch):
    expired_date = (date.today() - timedelta(days=400)).isoformat()
    projects = [
        _synthetic_project(banner="released", released_date=expired_date)
    ]
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
