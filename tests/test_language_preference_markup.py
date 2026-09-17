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


import main
from banner_lib import banner_markup_from_resolved


class _FakeEnv:
    def __init__(self, project_dir):
        self.project_dir = str(project_dir)
        self.variables = {}
        self.macros = {}

    def macro(self, func):
        self.macros[func.__name__] = func
        return func


def test_catalogue_heading_and_logo_opt_out_of_translate():
    heading = main.catalogue_card_heading(
        {"icon": "material-source-repository", "name": "Synthetic", "id": "synthetic"}
    )
    assert "translate=no" in heading
    env = _FakeEnv(ROOT)
    main.define_env(env)
    source = (ROOT / "src/main.py").read_text(encoding="utf-8")
    assert source.count('translate="no"') >= 3


def test_banner_version_opts_out_of_translate():
    markup = banner_markup_from_resolved(
        "Released",
        "green",
        "released",
        version="1.2.3",
    )
    assert 'class="catalogue-banner__version" translate="no"' in markup


def test_footer_hero_sponsor_quotes_opt_out_brand_names():
    footer = (ROOT / "overrides/partials/copyright.html").read_text(encoding="utf-8")
    index = (ROOT / "mkdocs/index.md").read_text(encoding="utf-8")
    sponsor = (ROOT / "mkdocs/sponsor.md").read_text(encoding="utf-8")
    quotes = (ROOT / "mkdocs/quotes.md").read_text(encoding="utf-8")
    assert 'translate="no"' in footer
    assert 'class="lupaxa-hero-title"' in index
    assert 'translate="no"' in index
    assert '<strong translate="no">The Lupaxa Project</strong>' in index
    assert '<strong translate="no">The Lupaxa Project</strong>' in sponsor
    assert 'class="quote-author" translate="no"' in quotes
    assert 'class="quote-year" translate="no"' in quotes
