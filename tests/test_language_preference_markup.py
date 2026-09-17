from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "overrides/partials/header.html").read_text(encoding="utf-8")
MKDOCS = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
NAV_CSS = (ROOT / "mkdocs/assets/stylesheets/30-navigation.css").read_text(
    encoding="utf-8"
)


def test_header_has_custom_picker_not_alternate():
    assert 'id="lupaxa-lang"' in HEADER
    assert "partials/alternate.html" not in HEADER
    assert "extra.alternate" not in HEADER
    assert 'translate="no"' in HEADER
    assert 'value="en"' in HEADER
    assert 'value="fr"' in HEADER
    assert 'value="de"' in HEADER
    assert 'id="lupaxa-lang-fallback"' in HEADER


def test_language_script_follows_page_lifecycle():
    scripts = [
        line.strip()
        for line in MKDOCS.splitlines()
        if line.strip().startswith("- assets/javascript/")
    ]
    assert "- assets/javascript/page-lifecycle.js" in scripts
    assert "- assets/javascript/language-preference.js" in scripts
    assert scripts.index("- assets/javascript/page-lifecycle.js") < scripts.index(
        "- assets/javascript/language-preference.js"
    )
    assert "extra.alternate" not in MKDOCS
    assert "mkdocs-static-i18n" not in MKDOCS
    assert "  language: en" in MKDOCS
    assert "social_locale: en_GB" in MKDOCS


def test_header_css_keeps_picker_out_of_nav_flex():
    assert ".lupaxa-lang-picker" in NAV_CSS
    assert ".lupaxa-lang-fallback" in NAV_CSS
