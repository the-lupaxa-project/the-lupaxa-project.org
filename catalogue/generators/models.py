"""Typed catalogue models used by the portal generator.

The loader returns plain dictionaries because it is responsible only for
reading YAML. After validation succeeds, this module converts those dictionaries
into predictable typed objects for rendering and export.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .loader import CatalogueData


@dataclass(frozen=True, slots=True)
class PortalDetails:
    """General information about the generated portal."""

    name: str
    description: str
    base_url: str
    github_url: str
    default_language: str = "en"


@dataclass(frozen=True, slots=True)
class CatalogueLink:
    """A named external link associated with a catalogue entry."""

    label: str
    url: str


@dataclass(frozen=True, slots=True)
class Category:
    """A curated portal category."""

    id: str
    name: str
    description: str
    group: str
    icon: str | None = None
    short_name: str | None = None
    featured: bool = False
    published: bool = False
    order: int = 999999

    @property
    def display_name(self) -> str:
        """Return the preferred short or full display name."""

        return self.short_name or self.name


@dataclass(frozen=True, slots=True)
class Organisation:
    """A curated GitHub organisation."""

    id: str
    name: str
    github_organisation: str
    github_url: str
    description: str
    type: str
    categories: tuple[str, ...] = ()
    documentation_url: str | None = None
    featured: bool = False
    published: bool = False
    order: int = 999999

    @property
    def links(self) -> tuple[CatalogueLink, ...]:
        """Return available links for the organisation."""

        links = [
            CatalogueLink(
                label="View on GitHub",
                url=self.github_url,
            )
        ]

        if self.documentation_url:
            links.append(
                CatalogueLink(
                    label="Documentation",
                    url=self.documentation_url,
                )
            )

        return tuple(links)


@dataclass(frozen=True, slots=True)
class Project:
    """A curated project entry."""

    id: str
    name: str
    repository: str
    description: str
    organisation: str
    categories: tuple[str, ...] = ()
    technologies: tuple[str, ...] = ()
    documentation_url: str | None = None
    repository_url: str | None = None
    status: str | None = None
    maturity: str | None = None
    visibility: str | None = None
    featured: bool = False
    published: bool = False
    order: int = 999999

    @property
    def links(self) -> tuple[CatalogueLink, ...]:
        """Return available links for the project."""

        links: list[CatalogueLink] = []

        if self.documentation_url:
            links.append(
                CatalogueLink(
                    label="Documentation",
                    url=self.documentation_url,
                )
            )

        if self.repository_url:
            links.append(
                CatalogueLink(
                    label="Repository",
                    url=self.repository_url,
                )
            )

        return tuple(links)


@dataclass(frozen=True, slots=True)
class Documentation:
    """A curated documentation entry."""

    id: str
    name: str
    description: str
    type: str
    categories: tuple[str, ...] = ()
    organisation: str | None = None
    project: str | None = None
    documentation_url: str | None = None
    repository_url: str | None = None
    featured: bool = False
    published: bool = False
    order: int = 999999

    @property
    def links(self) -> tuple[CatalogueLink, ...]:
        """Return available links for the documentation entry."""

        links: list[CatalogueLink] = []

        if self.documentation_url:
            links.append(
                CatalogueLink(
                    label="Read Documentation",
                    url=self.documentation_url,
                )
            )

        if self.repository_url:
            links.append(
                CatalogueLink(
                    label="Source Repository",
                    url=self.repository_url,
                )
            )

        return tuple(links)


@dataclass(frozen=True, slots=True)
class CatalogueGroup:
    """A configured group used to organise generated content."""

    id: str
    name: str
    description: str | None = None
    order: int = 999999


@dataclass(frozen=True, slots=True)
class PublicationSettings:
    """Catalogue publication behaviour."""

    published_field: str = "published"
    published_value: bool = True
    default_published: bool = False
    include_unpublished: bool = False


@dataclass(frozen=True, slots=True)
class OrderingSettings:
    """Catalogue ordering behaviour."""

    primary_field: str = "order"
    secondary_field: str = "name"
    missing_order: int = 999999


@dataclass(frozen=True, slots=True)
class FeaturedSettings:
    """Featured-content settings for one catalogue type."""

    enabled: bool = True
    maximum: int = 8


@dataclass(frozen=True, slots=True)
class PresentationSettings:
    """Presentation options used by the renderer."""

    show_categories: bool = True
    show_technologies: bool = True
    show_maturity: bool = True
    show_status: bool = True
    show_visibility: bool = False
    show_repository_links: bool = True
    show_documentation_links: bool = True
    show_empty_sections: bool = False
    external_links_in_new_tab: bool = False


@dataclass(frozen=True, slots=True)
class OutputPaths:
    """Configured generated-output paths."""

    projects: str
    organisations: str
    toolboxes: str
    documentation: str
    catalogue_data: str


@dataclass(frozen=True, slots=True)
class CatalogueConfiguration:
    """Typed generator configuration."""

    portal: PortalDetails
    output: OutputPaths
    publication: PublicationSettings
    ordering: OrderingSettings
    featured_projects: FeaturedSettings
    featured_organisations: FeaturedSettings
    featured_documentation: FeaturedSettings
    featured_categories: FeaturedSettings
    presentation: PresentationSettings
    organisation_groups: tuple[CatalogueGroup, ...]
    documentation_groups: tuple[CatalogueGroup, ...]
    category_groups: tuple[CatalogueGroup, ...]


@dataclass(frozen=True, slots=True)
class PortalCatalogue:
    """Complete typed portal catalogue."""

    configuration: CatalogueConfiguration
    projects: tuple[Project, ...]
    organisations: tuple[Organisation, ...]
    documentation: tuple[Documentation, ...]
    categories: tuple[Category, ...]

    category_index: Mapping[str, Category] = field(init=False, repr=False)
    organisation_index: Mapping[str, Organisation] = field(
        init=False,
        repr=False,
    )
    project_index: Mapping[str, Project] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        """Build immutable lookup indexes."""

        object.__setattr__(
            self,
            "category_index",
            {
                category.id: category
                for category in self.categories
            },
        )

        object.__setattr__(
            self,
            "organisation_index",
            {
                organisation.id: organisation
                for organisation in self.organisations
            },
        )

        object.__setattr__(
            self,
            "project_index",
            {
                project.id: project
                for project in self.projects
            },
        )

    @property
    def published_projects(self) -> tuple[Project, ...]:
        """Return published projects in configured order."""

        return self._published_and_sorted(self.projects)

    @property
    def published_organisations(self) -> tuple[Organisation, ...]:
        """Return published organisations in configured order."""

        return self._published_and_sorted(self.organisations)

    @property
    def published_documentation(self) -> tuple[Documentation, ...]:
        """Return published documentation entries in configured order."""

        return self._published_and_sorted(self.documentation)

    @property
    def published_categories(self) -> tuple[Category, ...]:
        """Return published categories in configured order."""

        return self._published_and_sorted(self.categories)

    @property
    def featured_projects(self) -> tuple[Project, ...]:
        """Return published featured projects."""

        settings = self.configuration.featured_projects

        if not settings.enabled:
            return ()

        entries = tuple(
            project
            for project in self.published_projects
            if project.featured
        )

        return entries[: settings.maximum]

    @property
    def featured_organisations(self) -> tuple[Organisation, ...]:
        """Return published featured organisations."""

        settings = self.configuration.featured_organisations

        if not settings.enabled:
            return ()

        entries = tuple(
            organisation
            for organisation in self.published_organisations
            if organisation.featured
        )

        return entries[: settings.maximum]

    @property
    def featured_documentation(self) -> tuple[Documentation, ...]:
        """Return published featured documentation entries."""

        settings = self.configuration.featured_documentation

        if not settings.enabled:
            return ()

        entries = tuple(
            documentation
            for documentation in self.published_documentation
            if documentation.featured
        )

        return entries[: settings.maximum]

    @property
    def featured_categories(self) -> tuple[Category, ...]:
        """Return published featured categories."""

        settings = self.configuration.featured_categories

        if not settings.enabled:
            return ()

        entries = tuple(
            category
            for category in self.published_categories
            if category.featured
        )

        return entries[: settings.maximum]

    def categories_for(
        self,
        category_ids: Iterable[str],
    ) -> tuple[Category, ...]:
        """Resolve category identifiers into category objects."""

        return tuple(
            category
            for category_id in category_ids
            if (category := self.category_index.get(category_id)) is not None
        )

    def organisation_for(
        self,
        organisation_id: str | None,
    ) -> Organisation | None:
        """Resolve an organisation identifier."""

        if organisation_id is None:
            return None

        return self.organisation_index.get(organisation_id)

    def project_for(
        self,
        project_id: str | None,
    ) -> Project | None:
        """Resolve a project identifier."""

        if project_id is None:
            return None

        return self.project_index.get(project_id)

    def projects_for_organisation(
        self,
        organisation_id: str,
        *,
        published_only: bool = True,
    ) -> tuple[Project, ...]:
        """Return projects associated with an organisation."""

        projects = (
            self.published_projects
            if published_only
            else self._sort_entries(self.projects)
        )

        return tuple(
            project
            for project in projects
            if project.organisation == organisation_id
        )

    def documentation_for_project(
        self,
        project_id: str,
        *,
        published_only: bool = True,
    ) -> tuple[Documentation, ...]:
        """Return documentation associated with a project."""

        entries = (
            self.published_documentation
            if published_only
            else self._sort_entries(self.documentation)
        )

        return tuple(
            documentation
            for documentation in entries
            if documentation.project == project_id
        )

    def documentation_for_organisation(
        self,
        organisation_id: str,
        *,
        published_only: bool = True,
    ) -> tuple[Documentation, ...]:
        """Return documentation associated with an organisation."""

        entries = (
            self.published_documentation
            if published_only
            else self._sort_entries(self.documentation)
        )

        return tuple(
            documentation
            for documentation in entries
            if documentation.organisation == organisation_id
        )

    def _published_and_sorted(
        self,
        entries: Iterable[Any],
    ) -> tuple[Any, ...]:
        """Filter and sort catalogue entries."""

        include_unpublished = (
            self.configuration.publication.include_unpublished
        )

        filtered = (
            entry
            for entry in entries
            if include_unpublished or entry.published
        )

        return self._sort_entries(filtered)

    def _sort_entries(
        self,
        entries: Iterable[Any],
    ) -> tuple[Any, ...]:
        """Sort entries by order and then name."""

        return tuple(
            sorted(
                entries,
                key=lambda entry: (
                    entry.order,
                    entry.name.casefold(),
                    entry.id,
                ),
            )
        )


def build_portal_catalogue(data: CatalogueData) -> PortalCatalogue:
    """Convert validated dictionary data into typed catalogue models.

    Args:
        data:
            Loaded and validated catalogue data.

    Returns:
        A complete typed portal catalogue.

    Notes:
        Validation should run before this function. This conversion assumes
        required fields exist and contain the expected types.
    """

    configuration = _build_configuration(data.config)

    return PortalCatalogue(
        configuration=configuration,
        projects=tuple(
            _build_project(entry)
            for entry in data.projects
        ),
        organisations=tuple(
            _build_organisation(entry)
            for entry in data.organisations
        ),
        documentation=tuple(
            _build_documentation(entry)
            for entry in data.documentation
        ),
        categories=tuple(
            _build_category(entry)
            for entry in data.categories
        ),
    )


def _build_configuration(
    config: dict[str, Any],
) -> CatalogueConfiguration:
    """Build the typed generator configuration."""

    portal = config["portal"]
    output = config["output"]
    publication = config["publication"]
    ordering = config["ordering"]
    featured = config.get("featured", {})
    presentation = config["presentation"]

    return CatalogueConfiguration(
        portal=PortalDetails(
            name=portal["name"],
            description=portal["description"],
            base_url=portal["base_url"],
            github_url=portal["github_url"],
            default_language=portal.get("default_language", "en"),
        ),
        output=OutputPaths(
            projects=output["projects"],
            organisations=output["organisations"],
            toolboxes=output["toolboxes"],
            documentation=output["documentation"],
            catalogue_data=output["catalogue_data"],
        ),
        publication=PublicationSettings(
            published_field=publication.get(
                "published_field",
                "published",
            ),
            published_value=publication.get(
                "published_value",
                True,
            ),
            default_published=publication.get(
                "default_published",
                False,
            ),
            include_unpublished=publication.get(
                "include_unpublished",
                False,
            ),
        ),
        ordering=OrderingSettings(
            primary_field=ordering.get(
                "primary_field",
                "order",
            ),
            secondary_field=ordering.get(
                "secondary_field",
                "name",
            ),
            missing_order=ordering.get(
                "missing_order",
                999999,
            ),
        ),
        featured_projects=_build_featured_settings(
            featured.get("projects"),
        ),
        featured_organisations=_build_featured_settings(
            featured.get("organisations"),
        ),
        featured_documentation=_build_featured_settings(
            featured.get("documentation"),
        ),
        featured_categories=_build_featured_settings(
            featured.get("categories"),
        ),
        presentation=PresentationSettings(
            show_categories=presentation.get(
                "show_categories",
                True,
            ),
            show_technologies=presentation.get(
                "show_technologies",
                True,
            ),
            show_maturity=presentation.get(
                "show_maturity",
                True,
            ),
            show_status=presentation.get(
                "show_status",
                True,
            ),
            show_visibility=presentation.get(
                "show_visibility",
                False,
            ),
            show_repository_links=presentation.get(
                "show_repository_links",
                True,
            ),
            show_documentation_links=presentation.get(
                "show_documentation_links",
                True,
            ),
            show_empty_sections=presentation.get(
                "show_empty_sections",
                False,
            ),
            external_links_in_new_tab=presentation.get(
                "external_links_in_new_tab",
                False,
            ),
        ),
        organisation_groups=_build_groups(
            config.get("organisation_groups", []),
        ),
        documentation_groups=_build_groups(
            config.get("documentation_groups", []),
        ),
        category_groups=_build_groups(
            config.get("category_groups", []),
        ),
    )


def _build_project(entry: dict[str, Any]) -> Project:
    """Build a project model from a catalogue entry."""

    return Project(
        id=entry["id"],
        name=entry["name"],
        repository=entry["repository"],
        description=entry["description"],
        organisation=entry["organisation"],
        categories=_to_string_tuple(entry.get("categories")),
        technologies=_to_string_tuple(entry.get("technologies")),
        documentation_url=entry.get("documentation_url"),
        repository_url=entry.get("repository_url"),
        status=entry.get("status"),
        maturity=entry.get("maturity"),
        visibility=entry.get("visibility"),
        featured=entry.get("featured", False),
        published=entry.get("published", False),
        order=entry.get("order", 999999),
    )


def _build_organisation(
    entry: dict[str, Any],
) -> Organisation:
    """Build an organisation model from a catalogue entry."""

    return Organisation(
        id=entry["id"],
        name=entry["name"],
        github_organisation=entry["github_organisation"],
        github_url=entry["github_url"],
        description=entry["description"],
        type=entry["type"],
        categories=_to_string_tuple(entry.get("categories")),
        documentation_url=entry.get("documentation_url"),
        featured=entry.get("featured", False),
        published=entry.get("published", False),
        order=entry.get("order", 999999),
    )


def _build_documentation(
    entry: dict[str, Any],
) -> Documentation:
    """Build a documentation model from a catalogue entry."""

    return Documentation(
        id=entry["id"],
        name=entry["name"],
        description=entry["description"],
        type=entry["type"],
        categories=_to_string_tuple(entry.get("categories")),
        organisation=entry.get("organisation"),
        project=entry.get("project"),
        documentation_url=entry.get("documentation_url"),
        repository_url=entry.get("repository_url"),
        featured=entry.get("featured", False),
        published=entry.get("published", False),
        order=entry.get("order", 999999),
    )


def _build_category(entry: dict[str, Any]) -> Category:
    """Build a category model from a catalogue entry."""

    return Category(
        id=entry["id"],
        name=entry["name"],
        description=entry["description"],
        group=entry["group"],
        icon=entry.get("icon"),
        short_name=entry.get("short_name"),
        featured=entry.get("featured", False),
        published=entry.get("published", False),
        order=entry.get("order", 999999),
    )


def _build_featured_settings(
    value: Any,
) -> FeaturedSettings:
    """Build featured-content settings from a mapping."""

    if not isinstance(value, dict):
        return FeaturedSettings()

    return FeaturedSettings(
        enabled=value.get("enabled", True),
        maximum=value.get("maximum", 8),
    )


def _build_groups(
    entries: Iterable[dict[str, Any]],
) -> tuple[CatalogueGroup, ...]:
    """Build and sort configured catalogue groups."""

    groups = tuple(
        CatalogueGroup(
            id=entry["id"],
            name=entry["name"],
            description=entry.get("description"),
            order=entry.get("order", 999999),
        )
        for entry in entries
    )

    return tuple(
        sorted(
            groups,
            key=lambda group: (
                group.order,
                group.name.casefold(),
                group.id,
            ),
        )
    )


def _to_string_tuple(value: Any) -> tuple[str, ...]:
    """Convert an optional list of strings into an immutable tuple."""

    if not isinstance(value, list):
        return ()

    return tuple(
        item
        for item in value
        if isinstance(item, str)
    )
