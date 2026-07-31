from pathlib import Path

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


def _filter_panel():
    env = _FakeEnv(ROOT)
    main.define_env(env)
    return env.macros["filter_panel"]


def test_filter_panel_status_options_project_lifecycle_only():
    filter_panel = _filter_panel()

    markup = filter_panel(
        "project",
        search_label="Search",
        search_placeholder="Search projects",
        summary_text="Showing all projects",
        include_status=True,
    )

    assert "Released" in markup
    assert "New Article" not in markup


def test_filter_panel_without_status_does_not_crash():
    filter_panel = _filter_panel()

    markup = filter_panel(
        "organisation",
        search_label="Search",
        search_placeholder="Search organisations",
        summary_text="Showing all organisations",
        include_status=False,
    )

    assert "filter-panel" in markup
    assert "Released" not in markup
