"""Markdown generation helpers for the catalogue renderer.

This module contains small, reusable helpers for producing predictable Markdown
without coupling the renderer to string-formatting details.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from abc import abstractmethod
from typing import Protocol


_WHITESPACE_PATTERN = re.compile(r"\s+")
_NON_ANCHOR_CHARACTER_PATTERN = re.compile(r"[^a-z0-9\- ]")
_MULTIPLE_HYPHEN_PATTERN = re.compile(r"-{2,}")


class LinkLike(Protocol):
    """Protocol implemented by objects that expose a label and URL."""

    @property
    @abstractmethod
    def label(self) -> str:
        """Return the link label."""
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> str:
        """Return the link URL."""
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class MarkdownLink:
    """A Markdown link definition."""

    label: str
    url: str


def heading(text: str, level: int = 1) -> str:
    """Return a Markdown heading.

    Args:
        text:
            Heading text.
        level:
            Heading depth between 1 and 6.

    Returns:
        A complete Markdown heading line.

    Raises:
        ValueError:
            If the heading level is outside the supported range.
    """

    if level < 1 or level > 6:
        raise ValueError("Markdown heading level must be between 1 and 6.")

    return f"{'#' * level} {text.strip()}"


def paragraph(text: str | None) -> str:
    """Normalise text for use as a Markdown paragraph."""

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.strip().splitlines()
    ]

    return " ".join(
        line
        for line in lines
        if line
    )


def markdown_link(label: str, url: str) -> str:
    """Return an inline Markdown link."""

    return f"[{escape_inline_text(label)}]({url})"


def link_list(
    links: Iterable[LinkLike | MarkdownLink],
    *,
    separator: str = " · ",
) -> str:
    """Render a compact inline list of Markdown links."""

    rendered = [
        markdown_link(link.label, link.url)
        for link in links
        if link.label and link.url
    ]

    return separator.join(rendered)


def bullet_list(
    values: Iterable[str],
    *,
    indent: int = 0,
) -> str:
    """Render a Markdown unordered list."""

    prefix = " " * indent

    return "\n".join(
        f"{prefix}- {value}"
        for value in values
    )


def definition_list(
    items: Iterable[tuple[str, str]],
) -> str:
    """Render a Material for MkDocs definition list."""

    sections: list[str] = []

    for term, definition in items:
        if not term or not definition:
            continue

        sections.extend(
            [
                term,
                f":   {definition}",
            ]
        )

    return "\n\n".join(sections)


def badge(label: str, value: str) -> str:
    """Render a small inline text badge.

    The output intentionally uses plain Markdown rather than third-party badge
    services so generated pages remain self-contained.
    """

    return f"**{escape_inline_text(label)}:** {escape_inline_text(value)}"


def metadata_line(
    values: Iterable[str],
    *,
    separator: str = " · ",
) -> str:
    """Render a compact metadata line, excluding empty values."""

    cleaned = [
        value.strip()
        for value in values
        if value and value.strip()
    ]

    return separator.join(cleaned)


def category_links(
    category_names: Iterable[tuple[str, str]],
    *,
    base_path: str = "../categories/",
) -> str:
    """Render category links from ``(identifier, display_name)`` pairs."""

    links = [
        markdown_link(
            display_name,
            f"{base_path}#{anchor(identifier)}",
        )
        for identifier, display_name in category_names
    ]

    return ", ".join(links)


def inline_code(value: str) -> str:
    """Render a value as inline Markdown code."""

    value = value.replace("`", "\\`")

    return f"`{value}`"


def escape_inline_text(value: str) -> str:
    """Escape characters that commonly affect inline Markdown."""

    replacements = {
        "\\": "\\\\",
        "*": "\\*",
        "_": "\\_",
        "[": "\\[",
        "]": "\\]",
    }

    escaped = value

    for character, replacement in replacements.items():
        escaped = escaped.replace(character, replacement)

    return escaped


def anchor(value: str) -> str:
    """Create a stable GitHub-style Markdown anchor."""

    normalised = value.strip().casefold()
    normalised = _WHITESPACE_PATTERN.sub(" ", normalised)
    normalised = _NON_ANCHOR_CHARACTER_PATTERN.sub("", normalised)
    normalised = normalised.replace(" ", "-")
    normalised = _MULTIPLE_HYPHEN_PATTERN.sub("-", normalised)

    return normalised.strip("-")


def front_matter(
    values: dict[str, str | bool | int | None],
) -> str:
    """Render simple YAML front matter.

    Values are quoted where needed to avoid accidental YAML coercion.
    """

    lines = ["---"]

    for key, value in values.items():
        if value is None:
            continue

        if isinstance(value, bool):
            rendered_value = "true" if value else "false"
        elif isinstance(value, int):
            rendered_value = str(value)
        else:
            rendered_value = _quote_yaml_string(value)

        lines.append(f"{key}: {rendered_value}")

    lines.append("---")

    return "\n".join(lines)


def admonition(
    title: str,
    body: str,
    *,
    kind: str = "info",
) -> str:
    """Render a Material for MkDocs admonition."""

    body_lines = body.strip().splitlines()

    indented_body = "\n".join(
        f"    {line}" if line else ""
        for line in body_lines
    )

    return (
        f'!!! {kind} "{title}"\n\n'
        f"{indented_body}"
    )


def card_grid(
    cards: Sequence[str],
    *,
    columns: int | None = None,
) -> str:
    """Render a Material for MkDocs card grid.

    Cards are supplied as complete Markdown fragments.
    """

    if not cards:
        return ""

    attribute = " grid cards"

    if columns is not None:
        attribute = f' grid cards columns="{columns}"'

    rendered_cards = "\n\n".join(
        _indent_block(card.strip(), 4)
        for card in cards
    )

    return (
        f'<div class="{attribute.strip()}">\n\n'
        f"{rendered_cards}\n\n"
        "</div>"
    )


def simple_card(
    title: str,
    description: str,
    *,
    icon: str | None = None,
    metadata: str | None = None,
    links: str | None = None,
) -> str:
    """Render a single Markdown card body."""

    title_parts: list[str] = []

    if icon:
        title_parts.append(f":{icon}:")

    title_parts.append(f"**{escape_inline_text(title)}**")

    sections = [
        " ".join(title_parts),
        "",
        paragraph(description),
    ]

    if metadata:
        sections.extend(
            [
                "",
                metadata,
            ]
        )

    if links:
        sections.extend(
            [
                "",
                links,
            ]
        )

    return "\n".join(sections).strip()


def markdown_table(
    headers: Sequence[str],
    rows: Iterable[Sequence[str]],
    *,
    alignments: Sequence[str] | None = None,
) -> str:
    """Render a Markdown table.

    Args:
        headers:
            Column headings.
        rows:
            Table rows.
        alignments:
            Optional alignment values: ``left``, ``centre`` or ``right``.
    """

    if not headers:
        return ""

    if alignments is None:
        alignments = tuple("left" for _ in headers)

    if len(alignments) != len(headers):
        raise ValueError(
            "Table alignment count must match the number of headers."
        )

    separator_cells = [
        _alignment_marker(alignment)
        for alignment in alignments
    ]

    lines = [
        "| " + " | ".join(_escape_table_cell(value) for value in headers) + " |",
        "| " + " | ".join(separator_cells) + " |",
    ]

    for row in rows:
        if len(row) != len(headers):
            raise ValueError(
                "Every Markdown table row must match the header column count."
            )

        lines.append(
            "| "
            + " | ".join(_escape_table_cell(value) for value in row)
            + " |"
        )

    return "\n".join(lines)


def join_sections(
    sections: Iterable[str | None],
    *,
    spacing: int = 2,
) -> str:
    """Join non-empty Markdown sections with consistent blank lines."""

    separator = "\n" * spacing

    clean_sections: list[str] = [
        section.strip()
        for section in sections
        if section and section.strip()
    ]

    return separator.join(clean_sections)

def _alignment_marker(alignment: str) -> str:
    """Return a Markdown table alignment marker."""

    normalised_alignment = alignment.casefold()

    if normalised_alignment == "left":
        return ":---"

    if normalised_alignment in {"centre", "center"}:
        return ":---:"

    if normalised_alignment == "right":
        return "---:"

    raise ValueError(
        "Table alignment must be left, centre, center or right."
    )


def _escape_table_cell(value: str) -> str:
    """Escape text for use inside a Markdown table cell."""

    return (
        value
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\n", "<br>")
    )


def _indent_block(value: str, spaces: int) -> str:
    """Indent every line in a block."""

    indentation = " " * spaces

    return "\n".join(
        f"{indentation}{line}" if line else ""
        for line in value.splitlines()
    )


def _quote_yaml_string(value: str) -> str:
    """Quote a string for the limited YAML front matter we emit."""

    escaped = (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
    )

    return f'"{escaped}"'
