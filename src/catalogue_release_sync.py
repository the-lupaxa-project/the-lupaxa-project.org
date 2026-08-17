"""Apply a GitHub Release onto an existing portal catalogue card."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

STABLE_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
CARD_SPLIT = re.compile(r"(?m)^- id: ")


@dataclass(frozen=True)
class SyncResult:
    status: str
    card_id: str | None
    card_name: str | None
    yaml_text: str


@dataclass(frozen=True)
class ReleaseResolution:
    skip: bool
    reason: str
    version: str | None = None
    released_date: str | None = None
    tag: str | None = None


def normalise_github_repo(value: str) -> str:
    text = (value or "").strip()
    if not text:
        return ""
    if "://" not in text and text.count("/") == 1:
        owner, repo = text.split("/", 1)
        return f"{owner.lower()}/{repo.removesuffix('.git').lower()}"
    parsed = urlparse(text)
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        return ""
    return f"{parts[0].lower()}/{parts[1].lower()}"


def version_from_tag(tag: str) -> str | None:
    match = STABLE_TAG.match((tag or "").strip())
    if not match:
        return None
    return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"


def format_released_date(published_at: str) -> str:
    text = (published_at or "").strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed.replace(tzinfo=None, microsecond=0).strftime("%Y-%m-%dT%H:%M:%S")


def resolve_stable_release(payload: dict[str, Any] | None) -> ReleaseResolution:
    if not payload or "tag_name" not in payload:
        return ReleaseResolution(True, "no_release")
    if payload.get("draft") or payload.get("prerelease"):
        return ReleaseResolution(True, "unstable")
    tag = str(payload.get("tag_name") or "")
    version = version_from_tag(tag)
    if not version:
        return ReleaseResolution(True, "unstable_tag")
    published = payload.get("published_at")
    if not published:
        return ReleaseResolution(True, "no_release")
    return ReleaseResolution(
        False,
        "ok",
        version=version,
        released_date=format_released_date(str(published)),
        tag=tag,
    )


def _cards(yaml_text: str) -> list[dict[str, Any]]:
    loaded = yaml.safe_load(yaml_text) or []
    if not isinstance(loaded, list):
        return []
    return [item for item in loaded if isinstance(item, dict)]


def _matching_cards(cards: list[dict[str, Any]], repository: str) -> list[dict[str, Any]]:
    key = normalise_github_repo(repository)
    return [
        card for card in cards if normalise_github_repo(str(card.get("repository") or "")) == key
    ]


def _replace_or_insert(block: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^  {re.escape(key)}:.*$")
    line = f'  {key}: "{value}"'
    if pattern.search(block):
        return pattern.sub(line, block, count=1)
    if not block.endswith("\n"):
        block += "\n"
    return block + line + "\n"


def _card_block(yaml_text: str, card_id: str) -> tuple[int, int]:
    matches = list(re.finditer(r"(?m)^- id: ([^\n]+)\n", yaml_text))
    for index, match in enumerate(matches):
        if match.group(1).strip() != card_id:
            continue
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(yaml_text)
        return start, end
    raise KeyError(card_id)


def apply_catalogue_release(
    yaml_text: str,
    *,
    repository: str,
    version: str,
    released_date: str,
) -> SyncResult:
    matches = _matching_cards(_cards(yaml_text), repository)
    if not matches:
        return SyncResult("not_found", None, None, yaml_text)
    if len(matches) > 1:
        return SyncResult("ambiguous", None, None, yaml_text)
    card = matches[0]
    if card.get("published", True) is False:
        return SyncResult(
            "unpublished",
            str(card.get("id") or "") or None,
            str(card.get("name") or "") or None,
            yaml_text,
        )
    card_id = str(card.get("id") or "")
    card_name = str(card.get("name") or "") or None
    if (
        card.get("banner") == "released"
        and str(card.get("version") or "") == version
        and str(card.get("released_date") or "") == released_date
    ):
        return SyncResult("unchanged", card_id, card_name, yaml_text)

    start, end = _card_block(yaml_text, card_id)
    block = yaml_text[start:end]
    block = _replace_or_insert(block, "banner", "released")
    # banner is an unquoted slug, not a quoted string
    block = re.sub(r'(?m)^  banner: "released"$', "  banner: released", block, count=1)
    block = _replace_or_insert(block, "version", version)
    block = _replace_or_insert(block, "released_date", released_date)
    return SyncResult(
        "updated",
        card_id,
        card_name,
        yaml_text[:start] + block + yaml_text[end:],
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("--file", type=Path, required=True)
    apply_cmd.add_argument("--repository", required=True)
    apply_cmd.add_argument("--version", required=True)
    apply_cmd.add_argument("--released-date", required=True)
    apply_cmd.add_argument(
        "--write",
        action="store_true",
        help="Write the file when status is updated",
    )
    sub.add_parser(
        "resolve",
        help="Read GitHub Release JSON from stdin; print skip/version fields",
    )
    return parser.parse_args(argv)


def _resolve_from_stdin() -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        payload: dict[str, Any] | None = None
    else:
        loaded = json.loads(raw)
        if not isinstance(loaded, dict):
            print("invalid release JSON", file=sys.stderr)
            return 1
        payload = loaded
    result = resolve_stable_release(payload)
    print(f"skip={'true' if result.skip else 'false'}")
    print(f"reason={result.reason}")
    if result.version:
        print(f"version={result.version}")
    if result.released_date:
        print(f"released_date={result.released_date}")
    if result.tag:
        print(f"tag={result.tag}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.command == "resolve":
        return _resolve_from_stdin()
    text = args.file.read_text(encoding="utf-8")
    result = apply_catalogue_release(
        text,
        repository=args.repository,
        version=args.version,
        released_date=args.released_date,
    )
    print(f"status={result.status}")
    if result.card_id:
        print(f"card_id={result.card_id}")
    if result.card_name:
        print(f"card_name={result.card_name}")
    if result.status == "updated" and args.write:
        args.file.write_text(result.yaml_text, encoding="utf-8")
    if result.status == "updated":
        return 0
    if result.status in {"unchanged", "not_found", "unpublished"}:
        return 2
    return 3


if __name__ == "__main__":
    sys.exit(main())
