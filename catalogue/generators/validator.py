"""Validate The Lupaxa Project portal catalogue.

This module performs catalogue-level validation after the YAML files have been
loaded. It checks required fields, identifiers, duplicate values, URLs, group
references and relationships between catalogue entries.

JSON Schema validation can be added later without changing the cross-reference
validation implemented here.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable
from urllib.parse import urlparse

from .loader import CatalogueData


IDENTIFIER_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ValidationSeverity(Enum):
    """Severity assigned to a validation message."""

    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single catalogue validation issue."""

    severity: ValidationSeverity
    catalogue: str
    message: str
    entry_id: str | None = None
    field: str | None = None

    def format(self) -> str:
        """Return a human-readable representation of the issue."""

        location_parts = [self.catalogue]

        if self.entry_id:
            location_parts.append(self.entry_id)

        if self.field:
            location_parts.append(self.field)

        location = ".".join(location_parts)

        return (
            f"[{self.severity.value.upper()}] "
            f"{location}: {self.message}"
        )


@dataclass(slots=True)
class ValidationResult:
    """Collection of validation issues."""

    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> list[ValidationIssue]:
        """Return all validation errors."""

        return [
            issue
            for issue in self.issues
            if issue.severity is ValidationSeverity.ERROR
        ]

    @property
    def warnings(self) -> list[ValidationIssue]:
        """Return all validation warnings."""

        return [
            issue
            for issue in self.issues
            if issue.severity is ValidationSeverity.WARNING
        ]

    @property
    def is_valid(self) -> bool:
        """Return whether the catalogue contains no validation errors."""

        return not self.errors

    def add_error(
        self,
        catalogue: str,
        message: str,
        *,
        entry_id: str | None = None,
        field: str | None = None,
    ) -> None:
        """Add an error to the result."""

        self.issues.append(
            ValidationIssue(
                severity=ValidationSeverity.ERROR,
                catalogue=catalogue,
                entry_id=entry_id,
                field=field,
                message=message,
            )
        )

    def add_warning(
        self,
        catalogue: str,
        message: str,
        *,
        entry_id: str | None = None,
        field: str | None = None,
    ) -> None:
        """Add a warning to the result."""

        self.issues.append(
            ValidationIssue(
                severity=ValidationSeverity.WARNING,
                catalogue=catalogue,
                entry_id=entry_id,
                field=field,
                message=message,
            )
        )


class CatalogueValidationError(RuntimeError):
    """Raised when catalogue validation fails."""

    def __init__(self, result: ValidationResult) -> None:
        """Initialise the exception from a validation result."""

        self.result = result

        message = (
            f"Catalogue validation failed with "
            f"{len(result.errors)} error(s) and "
            f"{len(result.warnings)} warning(s)."
        )

        super().__init__(message)


@dataclass(frozen=True, slots=True)
class ValidationOptions:
    """Validation behaviour derived from the catalogue configuration."""

    fail_on_error: bool = True
    fail_on_warning: bool = False
    require_unique_ids: bool = True
    require_known_categories: bool = True
    require_known_organisations: bool = True
    require_known_projects: bool = True
    require_known_group_types: bool = True
    require_urls_for_published_entries: bool = True

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> ValidationOptions:
        """Create validation options from the loaded configuration."""

        validation = config.get("validation", {})

        if not isinstance(validation, dict):
            return cls()

        return cls(
            fail_on_error=_get_boolean(
                validation,
                "fail_on_error",
                default=True,
            ),
            fail_on_warning=_get_boolean(
                validation,
                "fail_on_warning",
                default=False,
            ),
            require_unique_ids=_get_boolean(
                validation,
                "require_unique_ids",
                default=True,
            ),
            require_known_categories=_get_boolean(
                validation,
                "require_known_categories",
                default=True,
            ),
            require_known_organisations=_get_boolean(
                validation,
                "require_known_organisations",
                default=True,
            ),
            require_known_projects=_get_boolean(
                validation,
                "require_known_projects",
                default=True,
            ),
            require_known_group_types=_get_boolean(
                validation,
                "require_known_group_types",
                default=True,
            ),
            require_urls_for_published_entries=_get_boolean(
                validation,
                "require_urls_for_published_entries",
                default=True,
            ),
        )


@dataclass(frozen=True, slots=True)
class CatalogueIndexes:
    """Lookup indexes used during cross-reference validation."""

    project_ids: frozenset[str]
    organisation_ids: frozenset[str]
    category_ids: frozenset[str]
    organisation_group_ids: frozenset[str]
    documentation_group_ids: frozenset[str]
    category_group_ids: frozenset[str]


def validate_catalogue(
    data: CatalogueData,
    *,
    raise_on_failure: bool = False,
) -> ValidationResult:
    """Validate the complete catalogue.

    Args:
        data:
            Loaded catalogue data.
        raise_on_failure:
            Raise ``CatalogueValidationError`` when configured validation
            failure conditions are met.

    Returns:
        The complete validation result.

    Raises:
        CatalogueValidationError:
            If ``raise_on_failure`` is enabled and the configured failure
            threshold is reached.
    """

    result = ValidationResult()
    options = ValidationOptions.from_config(data.config)

    _validate_config(data.config, result)

    _validate_collection(
        catalogue_name="projects",
        entries=data.projects,
        required_fields=(
            "id",
            "name",
            "description",
            "organisation",
            "published",
            "order",
        ),
        result=result,
        require_unique_ids=options.require_unique_ids,
    )

    _validate_collection(
        catalogue_name="organisations",
        entries=data.organisations,
        required_fields=(
            "id",
            "name",
            "github_organisation",
            "github_url",
            "description",
            "type",
            "published",
            "order",
        ),
        result=result,
        require_unique_ids=options.require_unique_ids,
    )

    _validate_collection(
        catalogue_name="documentation",
        entries=data.documentation,
        required_fields=(
            "id",
            "name",
            "description",
            "type",
            "published",
            "order",
        ),
        result=result,
        require_unique_ids=options.require_unique_ids,
    )

    _validate_collection(
        catalogue_name="categories",
        entries=data.categories,
        required_fields=(
            "id",
            "name",
            "description",
            "group",
            "published",
            "order",
        ),
        result=result,
        require_unique_ids=options.require_unique_ids,
    )

    indexes = _build_indexes(data)

    _validate_projects(
        data.projects,
        indexes,
        result,
        options,
    )

    _validate_organisations(
        data.organisations,
        indexes,
        result,
        options,
    )

    _validate_documentation(
        data.documentation,
        indexes,
        result,
        options,
    )

    _validate_categories(
        data.categories,
        indexes,
        result,
        options,
    )

    should_fail = (
        options.fail_on_error
        and bool(result.errors)
    ) or (
        options.fail_on_warning
        and bool(result.warnings)
    )

    if raise_on_failure and should_fail:
        raise CatalogueValidationError(result)

    return result


def _validate_config(
    config: dict[str, Any],
    result: ValidationResult,
) -> None:
    """Validate the top-level generator configuration."""

    required_sections: tuple[str, ...] = (
        "portal",
        "catalogues",
        "output",
        "publication",
        "ordering",
        "validation",
        "presentation",
    )

    for section in required_sections:
        value = config.get(section)

        if value is None:
            result.add_error(
                "config",
                f"Missing required configuration section '{section}'.",
                field=section,
            )
            continue

        if not isinstance(value, dict):
            result.add_error(
                "config",
                f"Configuration section '{section}' must be a mapping.",
                field=section,
            )

    portal = config.get("portal")

    if isinstance(portal, dict):
        _require_non_empty_string(
            portal,
            "name",
            "config.portal",
            result,
        )

        _require_non_empty_string(
            portal,
            "description",
            "config.portal",
            result,
        )

        for field_name in ("base_url", "github_url"):
            value = portal.get(field_name)

            if value is None:
                result.add_error(
                    "config.portal",
                    "Required value is missing.",
                    field=field_name,
                )
            elif not _is_valid_http_url(value):
                result.add_error(
                    "config.portal",
                    "Value must be a valid HTTP or HTTPS URL.",
                    field=field_name,
                )

    _validate_group_definitions(
        config=config,
        section_name="organisation_groups",
        result=result,
    )

    _validate_group_definitions(
        config=config,
        section_name="documentation_groups",
        result=result,
    )

    _validate_group_definitions(
        config=config,
        section_name="category_groups",
        result=result,
    )


def _validate_collection(
    *,
    catalogue_name: str,
    entries: list[dict[str, Any]],
    required_fields: tuple[str, ...],
    result: ValidationResult,
    require_unique_ids: bool,
) -> None:
    """Perform common structural validation for a catalogue collection."""

    identifiers: dict[str, int] = {}

    for position, entry in enumerate(entries, start=1):
        entry_id = _entry_identifier(entry, position)

        for field_name in required_fields:
            if field_name not in entry:
                result.add_error(
                    catalogue_name,
                    "Required field is missing.",
                    entry_id=entry_id,
                    field=field_name,
                )

        identifier = entry.get("id")

        if identifier is not None:
            if not isinstance(identifier, str) or not identifier.strip():
                result.add_error(
                    catalogue_name,
                    "Identifier must be a non-empty string.",
                    entry_id=entry_id,
                    field="id",
                )
            elif not IDENTIFIER_PATTERN.fullmatch(identifier):
                result.add_error(
                    catalogue_name,
                    "Identifier must contain only lowercase letters, numbers "
                    "and single hyphens.",
                    entry_id=entry_id,
                    field="id",
                )
            else:
                identifiers[identifier] = identifiers.get(identifier, 0) + 1

        _validate_common_entry_fields(
            catalogue_name,
            entry,
            entry_id,
            result,
        )

    if require_unique_ids:
        for identifier, count in sorted(identifiers.items()):
            if count > 1:
                result.add_error(
                    catalogue_name,
                    f"Identifier is used by {count} entries.",
                    entry_id=identifier,
                    field="id",
                )


def _validate_common_entry_fields(
    catalogue_name: str,
    entry: dict[str, Any],
    entry_id: str,
    result: ValidationResult,
) -> None:
    """Validate common fields shared by catalogue entries."""

    for field_name in ("name", "description"):
        value = entry.get(field_name)

        if value is not None and (
            not isinstance(value, str)
            or not value.strip()
        ):
            result.add_error(
                catalogue_name,
                "Value must be a non-empty string.",
                entry_id=entry_id,
                field=field_name,
            )

    for field_name in ("published", "featured"):
        value = entry.get(field_name)

        if value is not None and not isinstance(value, bool):
            result.add_error(
                catalogue_name,
                "Value must be a boolean.",
                entry_id=entry_id,
                field=field_name,
            )

    order = entry.get("order")

    if order is not None and (
        not isinstance(order, int)
        or isinstance(order, bool)
        or order < 0
    ):
        result.add_error(
            catalogue_name,
            "Order must be a non-negative integer.",
            entry_id=entry_id,
            field="order",
        )

    categories = entry.get("categories")

    if categories is not None:
        _validate_identifier_list(
            catalogue_name=catalogue_name,
            entry_id=entry_id,
            field_name="categories",
            values=categories,
            result=result,
        )

    technologies = entry.get("technologies")

    if technologies is not None:
        _validate_string_list(
            catalogue_name=catalogue_name,
            entry_id=entry_id,
            field_name="technologies",
            values=technologies,
            result=result,
        )


def _validate_projects(
    projects: list[dict[str, Any]],
    indexes: CatalogueIndexes,
    result: ValidationResult,
    options: ValidationOptions,
) -> None:
    """Validate project-specific fields and references."""

    for position, project in enumerate(projects, start=1):
        entry_id = _entry_identifier(project, position)

        organisation = project.get("organisation")

        if (
            options.require_known_organisations
            and isinstance(organisation, str)
            and organisation not in indexes.organisation_ids
        ):
            result.add_error(
                "projects",
                f"Unknown organisation '{organisation}'.",
                entry_id=entry_id,
                field="organisation",
            )

        if options.require_known_categories:
            _validate_known_values(
                catalogue_name="projects",
                entry_id=entry_id,
                field_name="categories",
                values=project.get("categories"),
                known_values=indexes.category_ids,
                result=result,
            )

        _validate_urls(
            catalogue_name="projects",
            entry=project,
            entry_id=entry_id,
            fields=("repository_url", "documentation_url"),
            result=result,
        )

        if (
            options.require_urls_for_published_entries
            and project.get("published") is True
            and not _has_valid_url(
                project,
                ("repository_url", "documentation_url"),
            )
        ):
            result.add_error(
                "projects",
                "Published projects must define at least one valid repository "
                "or documentation URL.",
                entry_id=entry_id,
            )

        repository = project.get("repository")

        if repository is not None and (
            not isinstance(repository, str)
            or not repository.strip()
        ):
            result.add_error(
                "projects",
                "Repository must be a non-empty string.",
                entry_id=entry_id,
                field="repository",
            )


def _validate_organisations(
    organisations: list[dict[str, Any]],
    indexes: CatalogueIndexes,
    result: ValidationResult,
    options: ValidationOptions,
) -> None:
    """Validate organisation-specific fields and references."""

    github_organisations: dict[str, list[str]] = {}

    for position, organisation in enumerate(organisations, start=1):
        entry_id = _entry_identifier(organisation, position)

        organisation_type = organisation.get("type")

        if (
            options.require_known_group_types
            and isinstance(organisation_type, str)
            and organisation_type not in indexes.organisation_group_ids
        ):
            result.add_error(
                "organisations",
                f"Unknown organisation type '{organisation_type}'.",
                entry_id=entry_id,
                field="type",
            )

        if options.require_known_categories:
            _validate_known_values(
                catalogue_name="organisations",
                entry_id=entry_id,
                field_name="categories",
                values=organisation.get("categories"),
                known_values=indexes.category_ids,
                result=result,
            )

        _validate_urls(
            catalogue_name="organisations",
            entry=organisation,
            entry_id=entry_id,
            fields=("github_url", "documentation_url"),
            result=result,
        )

        if (
            options.require_urls_for_published_entries
            and organisation.get("published") is True
            and not _is_valid_http_url(organisation.get("github_url"))
        ):
            result.add_error(
                "organisations",
                "Published organisations must define a valid GitHub URL.",
                entry_id=entry_id,
                field="github_url",
            )

        github_name = organisation.get("github_organisation")

        if isinstance(github_name, str) and github_name.strip():
            github_organisations.setdefault(
                github_name.casefold(),
                [],
            ).append(entry_id)

    for github_name, entry_ids in sorted(github_organisations.items()):
        if len(entry_ids) > 1:
            result.add_warning(
                "organisations",
                "GitHub organisation is referenced by multiple catalogue "
                f"entries: {', '.join(entry_ids)}.",
                entry_id=github_name,
                field="github_organisation",
            )


def _validate_documentation(
    documentation_entries: list[dict[str, Any]],
    indexes: CatalogueIndexes,
    result: ValidationResult,
    options: ValidationOptions,
) -> None:
    """Validate documentation-specific fields and references."""

    for position, documentation in enumerate(
        documentation_entries,
        start=1,
    ):
        entry_id = _entry_identifier(documentation, position)

        documentation_type = documentation.get("type")

        if (
            options.require_known_group_types
            and isinstance(documentation_type, str)
            and documentation_type not in indexes.documentation_group_ids
        ):
            result.add_error(
                "documentation",
                f"Unknown documentation type '{documentation_type}'.",
                entry_id=entry_id,
                field="type",
            )

        organisation = documentation.get("organisation")

        if (
            options.require_known_organisations
            and organisation is not None
            and isinstance(organisation, str)
            and organisation not in indexes.organisation_ids
        ):
            result.add_error(
                "documentation",
                f"Unknown organisation '{organisation}'.",
                entry_id=entry_id,
                field="organisation",
            )

        project = documentation.get("project")

        if (
            options.require_known_projects
            and project is not None
            and isinstance(project, str)
            and project not in indexes.project_ids
        ):
            result.add_error(
                "documentation",
                f"Unknown project '{project}'.",
                entry_id=entry_id,
                field="project",
            )

        if options.require_known_categories:
            _validate_known_values(
                catalogue_name="documentation",
                entry_id=entry_id,
                field_name="categories",
                values=documentation.get("categories"),
                known_values=indexes.category_ids,
                result=result,
            )

        _validate_urls(
            catalogue_name="documentation",
            entry=documentation,
            entry_id=entry_id,
            fields=("documentation_url", "repository_url"),
            result=result,
        )

        if (
            options.require_urls_for_published_entries
            and documentation.get("published") is True
            and not _has_valid_url(
                documentation,
                ("documentation_url", "repository_url"),
            )
        ):
            result.add_error(
                "documentation",
                "Published documentation must define at least one valid "
                "documentation or repository URL.",
                entry_id=entry_id,
            )


def _validate_categories(
    categories: list[dict[str, Any]],
    indexes: CatalogueIndexes,
    result: ValidationResult,
    options: ValidationOptions,
) -> None:
    """Validate category-specific fields and references."""

    for position, category in enumerate(categories, start=1):
        entry_id = _entry_identifier(category, position)

        group = category.get("group")

        if (
            options.require_known_group_types
            and isinstance(group, str)
            and group not in indexes.category_group_ids
        ):
            result.add_error(
                "categories",
                f"Unknown category group '{group}'.",
                entry_id=entry_id,
                field="group",
            )

        icon = category.get("icon")

        if icon is not None and (
            not isinstance(icon, str)
            or not icon.strip()
        ):
            result.add_error(
                "categories",
                "Icon must be a non-empty string.",
                entry_id=entry_id,
                field="icon",
            )


def _build_indexes(data: CatalogueData) -> CatalogueIndexes:
    """Build lookup indexes from the loaded catalogue."""

    return CatalogueIndexes(
        project_ids=frozenset(_collect_identifiers(data.projects)),
        organisation_ids=frozenset(
            _collect_identifiers(data.organisations)
        ),
        category_ids=frozenset(_collect_identifiers(data.categories)),
        organisation_group_ids=frozenset(
            _collect_group_identifiers(
                data.config,
                "organisation_groups",
            )
        ),
        documentation_group_ids=frozenset(
            _collect_group_identifiers(
                data.config,
                "documentation_groups",
            )
        ),
        category_group_ids=frozenset(
            _collect_group_identifiers(
                data.config,
                "category_groups",
            )
        ),
    )


def _validate_group_definitions(
    *,
    config: dict[str, Any],
    section_name: str,
    result: ValidationResult,
) -> None:
    """Validate configured group definitions."""

    groups = config.get(section_name)

    if groups is None:
        result.add_error(
            "config",
            f"Missing required group section '{section_name}'.",
            field=section_name,
        )
        return

    if not isinstance(groups, list):
        result.add_error(
            "config",
            "Group section must be a list.",
            field=section_name,
        )
        return

    identifiers: dict[str, int] = {}

    for position, group in enumerate(groups, start=1):
        entry_id = f"entry-{position}"

        if not isinstance(group, dict):
            result.add_error(
                f"config.{section_name}",
                "Group entry must be a mapping.",
                entry_id=entry_id,
            )
            continue

        identifier = group.get("id")

        if isinstance(identifier, str) and identifier.strip():
            entry_id = identifier
            identifiers[identifier] = identifiers.get(identifier, 0) + 1

            if not IDENTIFIER_PATTERN.fullmatch(identifier):
                result.add_error(
                    f"config.{section_name}",
                    "Identifier must contain only lowercase letters, numbers "
                    "and single hyphens.",
                    entry_id=entry_id,
                    field="id",
                )
        else:
            result.add_error(
                f"config.{section_name}",
                "Group identifier must be a non-empty string.",
                entry_id=entry_id,
                field="id",
            )

        _require_non_empty_string(
            group,
            "name",
            f"config.{section_name}",
            result,
            entry_id=entry_id,
        )

        order = group.get("order")

        if order is None:
            result.add_error(
                f"config.{section_name}",
                "Required value is missing.",
                entry_id=entry_id,
                field="order",
            )
        elif (
            not isinstance(order, int)
            or isinstance(order, bool)
            or order < 0
        ):
            result.add_error(
                f"config.{section_name}",
                "Order must be a non-negative integer.",
                entry_id=entry_id,
                field="order",
            )

    for identifier, count in sorted(identifiers.items()):
        if count > 1:
            result.add_error(
                f"config.{section_name}",
                f"Identifier is used by {count} groups.",
                entry_id=identifier,
                field="id",
            )


def _validate_urls(
    *,
    catalogue_name: str,
    entry: dict[str, Any],
    entry_id: str,
    fields: tuple[str, ...],
    result: ValidationResult,
) -> None:
    """Validate URL fields when present."""

    for field_name in fields:
        value = entry.get(field_name)

        if value is None:
            continue

        if not _is_valid_http_url(value):
            result.add_error(
                catalogue_name,
                "Value must be a valid HTTP or HTTPS URL.",
                entry_id=entry_id,
                field=field_name,
            )


def _validate_known_values(
    *,
    catalogue_name: str,
    entry_id: str,
    field_name: str,
    values: Any,
    known_values: frozenset[str],
    result: ValidationResult,
) -> None:
    """Validate that values in a list exist in a known identifier set."""

    if not isinstance(values, list):
        return

    for value in values:
        if isinstance(value, str) and value not in known_values:
            result.add_error(
                catalogue_name,
                f"Unknown value '{value}'.",
                entry_id=entry_id,
                field=field_name,
            )


def _validate_identifier_list(
    *,
    catalogue_name: str,
    entry_id: str,
    field_name: str,
    values: Any,
    result: ValidationResult,
) -> None:
    """Validate a list of catalogue identifiers."""

    if not isinstance(values, list):
        result.add_error(
            catalogue_name,
            "Value must be a list.",
            entry_id=entry_id,
            field=field_name,
        )
        return

    seen: set[str] = set()

    for position, value in enumerate(values, start=1):
        if not isinstance(value, str) or not value.strip():
            result.add_error(
                catalogue_name,
                f"List item {position} must be a non-empty string.",
                entry_id=entry_id,
                field=field_name,
            )
            continue

        if not IDENTIFIER_PATTERN.fullmatch(value):
            result.add_error(
                catalogue_name,
                f"List item '{value}' is not a valid identifier.",
                entry_id=entry_id,
                field=field_name,
            )

        if value in seen:
            result.add_warning(
                catalogue_name,
                f"Duplicate list value '{value}'.",
                entry_id=entry_id,
                field=field_name,
            )

        seen.add(value)


def _validate_string_list(
    *,
    catalogue_name: str,
    entry_id: str,
    field_name: str,
    values: Any,
    result: ValidationResult,
) -> None:
    """Validate a list containing non-empty strings."""

    if not isinstance(values, list):
        result.add_error(
            catalogue_name,
            "Value must be a list.",
            entry_id=entry_id,
            field=field_name,
        )
        return

    normalised_values: set[str] = set()

    for position, value in enumerate(values, start=1):
        if not isinstance(value, str) or not value.strip():
            result.add_error(
                catalogue_name,
                f"List item {position} must be a non-empty string.",
                entry_id=entry_id,
                field=field_name,
            )
            continue

        normalised = value.strip().casefold()

        if normalised in normalised_values:
            result.add_warning(
                catalogue_name,
                f"Duplicate list value '{value}'.",
                entry_id=entry_id,
                field=field_name,
            )

        normalised_values.add(normalised)


def _require_non_empty_string(
    mapping: dict[str, Any],
    field_name: str,
    catalogue_name: str,
    result: ValidationResult,
    *,
    entry_id: str | None = None,
) -> None:
    """Require a non-empty string in a mapping."""

    value = mapping.get(field_name)

    if value is None:
        result.add_error(
            catalogue_name,
            "Required value is missing.",
            entry_id=entry_id,
            field=field_name,
        )
    elif not isinstance(value, str) or not value.strip():
        result.add_error(
            catalogue_name,
            "Value must be a non-empty string.",
            entry_id=entry_id,
            field=field_name,
        )


def _collect_identifiers(
    entries: Iterable[dict[str, Any]],
) -> set[str]:
    """Collect valid string identifiers from catalogue entries."""

    return {
        identifier
        for entry in entries
        if isinstance((identifier := entry.get("id")), str)
        and identifier.strip()
    }


def _collect_group_identifiers(
    config: dict[str, Any],
    section_name: str,
) -> set[str]:
    """Collect group identifiers from a configuration section."""

    groups = config.get(section_name)

    if not isinstance(groups, list):
        return set()

    return {
        identifier
        for group in groups
        if isinstance(group, dict)
        and isinstance((identifier := group.get("id")), str)
        and identifier.strip()
    }


def _entry_identifier(
    entry: dict[str, Any],
    position: int,
) -> str:
    """Return an entry identifier suitable for validation messages."""

    identifier = entry.get("id")

    if isinstance(identifier, str) and identifier.strip():
        return identifier

    return f"entry-{position}"


def _has_valid_url(
    entry: dict[str, Any],
    fields: tuple[str, ...],
) -> bool:
    """Return whether any supplied field contains a valid URL."""

    return any(
        _is_valid_http_url(entry.get(field_name))
        for field_name in fields
    )


def _is_valid_http_url(value: Any) -> bool:
    """Return whether a value is a valid absolute HTTP or HTTPS URL."""

    if not isinstance(value, str) or not value.strip():
        return False

    parsed = urlparse(value.strip())

    return (
        parsed.scheme in {"http", "https"}
        and bool(parsed.netloc)
        and " " not in value
    )


def _get_boolean(
    mapping: dict[str, Any],
    key: str,
    *,
    default: bool,
) -> bool:
    """Read a boolean configuration value with a safe default."""

    value = mapping.get(key, default)

    return value if isinstance(value, bool) else default
