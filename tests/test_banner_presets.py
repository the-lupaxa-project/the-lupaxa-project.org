from banner_lib import (
    ARTICLE_BANNER_PRESETS,
    DEFAULT_PROJECT_VERSION,
    PROJECT_BANNER_PRESETS,
    banner_markup,
    normalise_project_version,
    resolve_banner,
    resolve_project_version,
)

EXPECTED_PROJECT = {
    "in-planning": ("In Planning", "green"),
    "in-development": ("In Development", "purple"),
    "in-testing": ("In Testing", "neutral"),
    "in-review": ("In Review", "orange"),
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
    assert resolve_banner({"status": "in-testing", "label": "QA", "tone": "orange"}) == (
        "QA",
        "orange",
        "in-testing",
    )


def test_normalise_project_version():
    assert normalise_project_version("1.2.0") == "1.2.0"
    assert normalise_project_version("v1.2.0") == "1.2.0"
    assert normalise_project_version("V2.0") == "2.0"
    assert normalise_project_version("") is None
    assert normalise_project_version(None) is None


def test_resolve_project_version_defaults_to_semver_start():
    assert DEFAULT_PROJECT_VERSION == "0.1.0"
    assert resolve_project_version(None) == "0.1.0"
    assert resolve_project_version("1.2.0") == "1.2.0"


def test_project_banner_includes_version_on_every_preset():
    html = banner_markup(
        "in-testing",
        presets=PROJECT_BANNER_PRESETS,
        version="1.2.0",
        default_version=DEFAULT_PROJECT_VERSION,
    )
    assert "In Testing" in html
    assert "v1.2.0" in html
    assert "catalogue-banner--with-version" in html
    assert 'data-banner-status="in-testing"' in html


def test_project_banner_defaults_missing_version():
    html = banner_markup(
        "in-review",
        presets=PROJECT_BANNER_PRESETS,
        default_version=DEFAULT_PROJECT_VERSION,
    )
    assert "v0.1.0" in html
    assert "In Review" in html
