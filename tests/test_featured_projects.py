"""Featured projects home macro."""

from pathlib import Path

import main

ROOT = Path(__file__).resolve().parent.parent


class _FakeEnv:
    def __init__(self, project_dir: Path) -> None:
        self.project_dir = str(project_dir)
        self.variables: dict = {}
        self.macros: dict = {}

    def macro(self, func):
        self.macros[func.__name__] = func
        return func


def test_featured_projects_includes_sort_bar():
    env = _FakeEnv(ROOT)
    main.define_env(env)
    markup = env.macros["featured_projects"]()

    assert "featured-projects-header" in markup
    assert 'id="featured-projects"' in markup
    assert "Featured Projects" in markup
    assert "data-featured-sort-bar" in markup
    assert "data-featured-catalogue" in markup
    assert 'data-featured-sort="alpha"' in markup
    assert 'data-featured-sort="newest"' in markup
    assert "A–Z" in markup
    assert "Newest" in markup
