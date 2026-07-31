from banner_lib import (
    ARTICLE_BANNER_PRESETS,
    BANNER_PRESETS,
    PROJECT_BANNER_PRESETS,
    resolve_banner,
)

EXPECTED_PROJECT = {
    "in-planning": ("In Planning", "green"),
    "in-development": ("In Development", "purple"),
    "in-testing": ("In Testing", "neutral"),
    "closed-alpha": ("Closed Alpha", "red"),
    "open-beta": ("Open Beta", "orange"),
    "released": ("Released", "blue"),
}


def test_project_presets():
    assert PROJECT_BANNER_PRESETS == EXPECTED_PROJECT


def test_article_new_preset():
    assert ARTICLE_BANNER_PRESETS["new"] == ("New Article", "blue")


def test_resolve_banner_string_presets():
    for slug, (label, tone) in EXPECTED_PROJECT.items():
        assert resolve_banner(slug) == (label, tone, slug)
    assert resolve_banner("new") == ("New Article", "blue", "new")


def test_unknown_preset_string_does_not_resolve():
    assert resolve_banner("coming-soon") is None


def test_custom_override_still_works():
    assert resolve_banner(
        {"status": "in-testing", "label": "QA", "tone": "orange"}
    ) == ("QA", "orange", "in-testing")
