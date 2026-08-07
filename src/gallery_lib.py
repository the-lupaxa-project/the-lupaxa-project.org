from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


def load_gallery_data(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("gallery.yml must be a mapping at the top level")
    return data


def published_entries(data: dict[str, Any]) -> list[dict[str, Any]]:
    entries = data.get("entries") or []
    return [entry for entry in entries if entry.get("published", True)]


def validate_gallery(data: dict[str, Any]) -> None:
    entries = data.get("entries") or []
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, Mapping):
            raise ValueError(f"Gallery entry {index} must be a mapping")
        if not entry.get("published", True):
            continue
        has_image = bool(entry.get("image"))
        has_video = bool(entry.get("video"))
        if not has_image and not has_video:
            raise ValueError(
                f"Published gallery entry {index} missing required field(s): image or video"
            )
        if entry.get("tags") is not None and not isinstance(entry["tags"], list):
            raise ValueError(f"Published gallery entry {index} field 'tags' must be a list")


def collect_tags(entries: list[dict[str, Any]]) -> list[str]:
    # Media filters are rendered separately (images / videos), not as dynamic tags.
    reserved = {"images", "videos"}
    tags: set[str] = set()
    for entry in entries:
        for tag in entry.get("tags") or []:
            name = str(tag)
            if name not in reserved:
                tags.add(name)
    return sorted(tags)


def is_remote_media(path: str) -> bool:
    value = (path or "").strip().lower()
    return value.startswith("http://") or value.startswith("https://")
