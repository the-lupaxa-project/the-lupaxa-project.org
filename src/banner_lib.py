"""Shared catalogue status banners and expiry helpers."""

from __future__ import annotations

import html
from datetime import date, datetime, timezone
from typing import Any

PROJECT_BANNER_PRESETS: dict[str, tuple[str, str]] = {
    "in-planning": ("In Planning", "green"),
    "in-development": ("In Development", "purple"),
    "in-testing": ("In Testing", "neutral"),
    "in-review": ("In Review", "orange"),
    "closed-alpha": ("Closed Alpha", "red"),
    "open-beta": ("Open Beta", "orange"),
    "released": ("Released", "blue"),
}
ARTICLE_BANNER_PRESETS: dict[str, tuple[str, str]] = {
    "new": ("New Article", "blue"),
}
POLICY_BANNER_PRESETS: dict[str, tuple[str, str]] = {
    "new": ("New Policy", "blue"),
    "updated": ("Updated Policy", "purple"),
}
# Deliberately not merged into BANNER_PRESETS — the "new" slug clashes with
# ARTICLE_BANNER_PRESETS, and policy resolve/markup calls always pass
# presets=POLICY_BANNER_PRESETS explicitly so labels never leak across kinds.
BANNER_PRESETS: dict[str, tuple[str, str]] = {
    **PROJECT_BANNER_PRESETS,
    **ARTICLE_BANNER_PRESETS,
}
BANNER_TONES = frozenset({"red", "green", "purple", "blue", "orange", "neutral"})
DEFAULT_BANNER_EXPIRY_DAYS = 28


def parse_iso_datetime(value: Any) -> datetime | None:
    """Parse an ISO calendar date or date-time into a ``datetime``.

    Date-only values (``YYYY-MM-DD``) become midnight on that day. Strings may
    use ``T`` or a space between date and time. Banner expiry still uses the
    calendar date via :func:`parse_iso_date`; newest-project sorting uses the
    full timestamp.
    """

    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip().replace(" ", "T", 1)
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def parse_iso_date(value: Any) -> date | None:
    """Parse an ISO date or date-time and return the calendar date."""

    parsed = parse_iso_datetime(value)
    return parsed.date() if parsed is not None else None


def format_publish_date_attr(value: Any) -> str | None:
    """Format ``data-publish-date`` for catalogue cards.

    Date-only inputs stay ``YYYY-MM-DD``. Values with a time use UTC
    ``YYYY-MM-DDTHH:MM:SS`` so client-side newest sort can break same-day ties.
    """

    if isinstance(value, datetime):
        dt = value
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt.replace(microsecond=0).isoformat(sep="T")
    if isinstance(value, date):
        return value.isoformat()
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    parsed = parse_iso_datetime(text)
    if parsed is None:
        return None
    normalised = text.replace(" ", "T", 1)
    if "T" in normalised and len(text) > 10:
        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed.replace(microsecond=0).isoformat(sep="T")
    return parsed.date().isoformat()


def banner_still_active(
    event_date: date | None,
    *,
    today: date,
    expiry_days: int,
) -> bool:
    if event_date is None:
        return False
    delta = (today - event_date).days
    if delta < 0:
        return True
    return delta <= expiry_days


def _banner_filter_key(status: str | None, label: str) -> str:
    if status:
        return status
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in label)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-")


def resolve_banner(
    raw: Any,
    *,
    presets: dict[str, tuple[str, str]] | None = None,
) -> tuple[str, str, str] | None:
    presets = presets if presets is not None else BANNER_PRESETS
    if raw is None or raw is False:
        return None
    status: str | None = None
    label: str | None = None
    tone: str | None = None
    if isinstance(raw, str):
        status = raw.strip() or None
    elif isinstance(raw, dict):
        status_val = raw.get("status")
        if isinstance(status_val, str) and status_val.strip():
            status = status_val.strip()
        label_val = raw.get("label")
        if isinstance(label_val, str) and label_val.strip():
            label = label_val.strip()
        tone_val = raw.get("tone")
        if isinstance(tone_val, str) and tone_val.strip():
            tone = tone_val.strip()
    else:
        return None
    preset = presets.get(status) if status else None
    if label is None and preset:
        label = preset[0]
    if tone is None and preset:
        tone = preset[1]
    if tone is None or tone not in BANNER_TONES:
        tone = "neutral"
    if not label:
        return None
    # Unknown bare string with no preset and no explicit label → None
    if isinstance(raw, str) and preset is None:
        return None
    return label, tone, _banner_filter_key(status, label)


def banner_markup_from_resolved(label: str, tone: str, filter_key: str) -> str:
    safe_label = html.escape(label, quote=True)
    safe_key = html.escape(filter_key, quote=True)
    length_class = " catalogue-banner--short" if len(label) <= 5 else ""
    return (
        f'    <span class="catalogue-banner catalogue-banner--{tone}{length_class}" '
        f'data-banner-status="{safe_key}" '
        f'data-banner-label="{safe_label}" '
        f'aria-label="Status: {safe_label}" '
        f'role="button" tabindex="0">'
        f'<span class="catalogue-banner__band" aria-hidden="true">'
        f'<span class="catalogue-banner__text">{safe_label}</span>'
        f"</span></span>"
    )


def banner_markup(
    raw: Any,
    *,
    presets: dict[str, tuple[str, str]] | None = None,
    event_date: date | None = None,
    today: date | None = None,
    expiry_days: int | None = None,
    time_limited_statuses: frozenset[str] = frozenset({"released", "new"}),
) -> str:
    resolved = resolve_banner(raw, presets=presets)
    if not resolved:
        return ""
    label, tone, filter_key = resolved
    if filter_key in time_limited_statuses:
        days = DEFAULT_BANNER_EXPIRY_DAYS if expiry_days is None else expiry_days
        day = today or date.today()
        if not banner_still_active(event_date, today=day, expiry_days=days):
            return ""
    return banner_markup_from_resolved(label, tone, filter_key)
