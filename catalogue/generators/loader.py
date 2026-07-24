"""Load The Lupaxa Project portal catalogue files.

This module is responsible only for reading YAML files and performing basic
structural checks. Detailed schema and cross-reference validation will be
handled separately by the validator module.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class CatalogueLoadError(RuntimeError):
    """Raised when a catalogue file cannot be loaded."""


@dataclass(frozen=True, slots=True)
class CataloguePaths:
    """Resolved paths for the portal catalogue."""

    repository_root: Path
    catalogue_root: Path
    content_root: Path
    config: Path
    projects: Path
    organisations: Path
    documentation: Path
    categories: Path

    @classmethod
    def from_repository_root(cls, repository_root: Path) -> CataloguePaths:
        """Create the standard catalogue paths for a repository."""

        repository_root = repository_root.resolve()
        catalogue_root = repository_root / "catalogue"
        content_root = catalogue_root / "content"

        return cls(
            repository_root=repository_root,
            catalogue_root=catalogue_root,
            content_root=content_root,
            config=catalogue_root / "config.yml",
            projects=content_root / "projects.yml",
            organisations=content_root / "organisations.yml",
            documentation=content_root / "documentation.yml",
            categories=content_root / "categories.yml",
        )


@dataclass(slots=True)
class CatalogueData:
    """Loaded catalogue configuration and content."""

    config: dict[str, Any]
    projects: list[dict[str, Any]]
    organisations: list[dict[str, Any]]
    documentation: list[dict[str, Any]]
    categories: list[dict[str, Any]]


def find_repository_root(start: Path | None = None) -> Path:
    """Find the repository root containing ``mkdocs.yml`` and ``catalogue``.

    Args:
        start:
            Directory from which to begin searching. The current working
            directory is used when omitted.

    Returns:
        The resolved repository root path.

    Raises:
        CatalogueLoadError:
            If no suitable repository root can be found.
    """

    current = (start or Path.cwd()).resolve()

    if current.is_file():
        current = current.parent

    for candidate in (current, *current.parents):
        if (
            (candidate / "mkdocs.yml").is_file()
            and (candidate / "catalogue").is_dir()
        ):
            return candidate

    raise CatalogueLoadError(
        "Could not locate the repository root. Expected to find both "
        "'mkdocs.yml' and a 'catalogue' directory."
    )


def load_yaml_file(path: Path) -> dict[str, Any]:
    """Load a YAML file and require a mapping at its root.

    Args:
        path:
            YAML file to load.

    Returns:
        The parsed YAML mapping.

    Raises:
        CatalogueLoadError:
            If the file is missing, unreadable, invalid, empty or does not
            contain a mapping at its root.
    """

    if not path.exists():
        raise CatalogueLoadError(f"Catalogue file does not exist: {path}")

    if not path.is_file():
        raise CatalogueLoadError(f"Catalogue path is not a file: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise CatalogueLoadError(
            f"Could not read catalogue file '{path}': {exc}"
        ) from exc

    try:
        loaded = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise CatalogueLoadError(
            f"Invalid YAML in catalogue file '{path}': {exc}"
        ) from exc

    if loaded is None:
        raise CatalogueLoadError(f"Catalogue file is empty: {path}")

    if not isinstance(loaded, dict):
        raise CatalogueLoadError(
            f"Catalogue file must contain a mapping at its root: {path}"
        )

    return loaded


def load_catalogue_list(
    path: Path,
    root_key: str,
) -> list[dict[str, Any]]:
    """Load a list of catalogue entries from a YAML file.

    Args:
        path:
            YAML file containing the catalogue.
        root_key:
            Mapping key containing the entry list.

    Returns:
        A list of catalogue entry mappings.

    Raises:
        CatalogueLoadError:
            If the root key is missing, is not a list, or contains values that
            are not mappings.
    """

    document = load_yaml_file(path)

    if root_key not in document:
        raise CatalogueLoadError(
            f"Catalogue file '{path}' is missing the required "
            f"'{root_key}' key."
        )

    entries = document[root_key]

    if not isinstance(entries, list):
        raise CatalogueLoadError(
            f"The '{root_key}' value in '{path}' must be a list."
        )

    invalid_positions = [
        index
        for index, entry in enumerate(entries, start=1)
        if not isinstance(entry, dict)
    ]

    if invalid_positions:
        positions = ", ".join(str(position) for position in invalid_positions)

        raise CatalogueLoadError(
            f"The '{root_key}' list in '{path}' contains non-mapping entries "
            f"at positions: {positions}."
        )

    return entries


def load_catalogue(
    repository_root: Path | None = None,
) -> tuple[CataloguePaths, CatalogueData]:
    """Load the complete curated portal catalogue.

    Args:
        repository_root:
            Repository root to use. The root is discovered automatically when
            omitted.

    Returns:
        A tuple containing the resolved catalogue paths and loaded data.

    Raises:
        CatalogueLoadError:
            If any required file cannot be loaded.
    """

    root = (
        repository_root.resolve()
        if repository_root is not None
        else find_repository_root()
    )

    paths = CataloguePaths.from_repository_root(root)

    data = CatalogueData(
        config=load_yaml_file(paths.config),
        projects=load_catalogue_list(paths.projects, "projects"),
        organisations=load_catalogue_list(
            paths.organisations,
            "organisations",
        ),
        documentation=load_catalogue_list(
            paths.documentation,
            "documentation",
        ),
        categories=load_catalogue_list(paths.categories, "categories"),
    )

    return paths, data
