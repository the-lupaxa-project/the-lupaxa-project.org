from main import BANNER_PRESETS, _resolve_banner


EXPECTED = {
    "in-planning": ("In planning", "green"),
    "in-development": ("In development", "purple"),
    "in-testing": ("In testing", "neutral"),
    "closed-alpha": ("Closed alpha", "red"),
    "open-beta": ("Open beta", "orange"),
    "released": ("Released", "blue"),
}


def test_banner_presets_match_lifecycle():
    assert set(BANNER_PRESETS) == set(EXPECTED)
    for slug, (label, tone) in EXPECTED.items():
        assert BANNER_PRESETS[slug] == (label, tone)


def test_resolve_banner_string_presets():
    for slug, (label, tone) in EXPECTED.items():
        assert _resolve_banner(slug) == (label, tone, slug)


def test_removed_presets_do_not_resolve_as_strings():
    assert _resolve_banner("coming-soon") is None
    assert _resolve_banner("new") is None


def test_custom_override_still_works():
    assert _resolve_banner(
        {"status": "in-testing", "label": "QA", "tone": "orange"}
    ) == ("QA", "orange", "in-testing")
