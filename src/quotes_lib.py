from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_quotes_data(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("quotes.yml must be a mapping at the top level")
    return data


def published_quotes(data: dict[str, Any]) -> list[dict[str, Any]]:
    quotes = data.get("quotes") or []
    return [q for q in quotes if q.get("published", True)]


def validate_quotes(data: dict[str, Any]) -> None:
    required_fields = ("text", "author", "card_color", "text_color")
    for index, quote in enumerate(published_quotes(data), start=1):
        missing = [field for field in required_fields if not quote.get(field)]
        if missing:
            fields = ", ".join(missing)
            raise ValueError(f"Published quote {index} missing required field(s): {fields}")


def collect_tags(quotes: list[dict[str, Any]]) -> list[str]:
    tags: set[str] = set()
    for quote in quotes:
        for tag in quote.get("tags") or []:
            tags.add(str(tag))
    return sorted(tags)
