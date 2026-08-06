from datetime import date

from banner_lib import banner_markup, banner_still_active, parse_iso_date


def test_parse_iso_date():
    assert parse_iso_date("2026-07-01") == date(2026, 7, 1)
    assert parse_iso_date(None) is None
    assert parse_iso_date("nope") is None


def test_banner_still_active_window():
    today = date(2026, 7, 31)
    assert banner_still_active(date(2026, 7, 31), today=today, expiry_days=28) is True
    assert banner_still_active(date(2026, 7, 3), today=today, expiry_days=28) is True
    assert banner_still_active(date(2026, 7, 2), today=today, expiry_days=28) is False
    assert banner_still_active(date(2026, 8, 5), today=today, expiry_days=28) is True  # future
    assert banner_still_active(None, today=today, expiry_days=28) is False


def test_released_markup_hidden_when_expired():
    html = banner_markup(
        "released",
        event_date=date(2020, 1, 1),
        today=date(2026, 7, 31),
        expiry_days=28,
        time_limited_statuses=frozenset({"released"}),
    )
    assert html == ""


def test_released_markup_shown_when_fresh():
    html = banner_markup(
        "released",
        event_date=date(2026, 7, 20),
        today=date(2026, 7, 31),
        expiry_days=28,
        time_limited_statuses=frozenset({"released"}),
    )
    assert "catalogue-banner--blue" in html
    assert "Released" in html


def test_new_article_markup():
    html = banner_markup(
        "new",
        presets={"new": ("New Article", "blue")},
        event_date=date(2026, 7, 20),
        today=date(2026, 7, 31),
        expiry_days=28,
        time_limited_statuses=frozenset({"new"}),
    )
    assert "New Article" in html
    assert 'data-banner-status="new"' in html
