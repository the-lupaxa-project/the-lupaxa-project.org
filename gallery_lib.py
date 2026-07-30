from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml


def load_photos_data(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError("photos.yml must be a mapping at the top level")
    return data


def published_photos(data: dict[str, Any]) -> list[dict[str, Any]]:
    photos = data.get("photos") or []
    return [p for p in photos if p.get("published", True)]


def validate_photos(data: dict[str, Any]) -> None:
    photos = data.get("photos") or []
    for index, photo in enumerate(photos, start=1):
        if not isinstance(photo, Mapping):
            raise ValueError(f"Photo entry {index} must be a mapping")
        if not photo.get("published", True):
            continue
        has_photo = bool(photo.get("photo"))
        has_video = bool(photo.get("video"))
        if not has_photo and not has_video:
            raise ValueError(
                f"Published photo {index} missing required field(s): photo or video"
            )
        if photo.get("tags") is not None and not isinstance(photo["tags"], list):
            raise ValueError(f"Published photo {index} field 'tags' must be a list")


def collect_tags(photos: list[dict[str, Any]]) -> list[str]:
    reserved = {"photos", "videos"}
    tags: set[str] = set()
    for photo in photos:
        for tag in photo.get("tags") or []:
            name = str(tag)
            if name not in reserved:
                tags.add(name)
    return sorted(tags)
