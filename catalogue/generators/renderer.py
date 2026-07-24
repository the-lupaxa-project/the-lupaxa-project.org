"""Render the curated catalogue as Markdown pages.

This module converts the typed portal catalogue into complete Markdown pages.
It does not write files directly. File output is handled by the generator entry
point so rendering can be tested independently.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from .markdown import (
    badge,
    heading,
    inline_code,
    join_sections,
    metadata_line,
    paragraph,
)
from .models import (
    CatalogueGroup,
    Documentation,
    Organisation,
    PortalCatalogue,
    Project,
)


@dataclass(frozen=True, slots=True)
class RenderedPage:
    """A generated Markdown page."""

    title: str
    content: str


class CatalogueRenderer:
    """Render catalogue entries into portal pages."""

    def __init__(self, catalogue: PortalCatalogue) -> None:
        """Initialise the renderer."""

        self.catalogue = catalogue
        self.configuration = catalogue.configuration
        self.presentation = catalogue.configuration.presentation

    def render_projects_page(self) -> RenderedPage:
        """Render the complete projects catalogue page."""

        projects = self.catalogue.published_projects

        sections: list[str | None] = [
            heading("Projects"),
            paragraph(
                "A curated catalogue of published projects contained across "
                "The Lupaxa Project ecosystem."
            ),
            self._render_project_summary(projects),
            self._render_featured_projects(),
            self._render_projects_by_organisation(projects),
        ]

        if not projects:
            sections.append(
                self._render_empty_message(
                    "No projects are currently published."
                )
            )

        return RenderedPage(
            title="Projects",
            content=self._finalise_page(sections),
        )

    def render_organisations_page(self) -> RenderedPage:
        """Render the complete organisations catalogue page."""

        organisations = tuple(
            organisation
            for organisation in self.catalogue.published_organisations
            if organisation.type != "toolbox"
        )

        sections: list[str | None] = [
            heading("Organisations"),
            paragraph(
                "The organisations that contain the shared resources, "
                "projects and experimental work published by "
                "The Lupaxa Project."
            ),
            self._render_organisation_summary(organisations),
            self._render_featured_organisations(
                exclude_types={"toolbox"},
            ),
            self._render_organisations_by_group(
                organisations,
                excluded_group_ids={"toolbox"},
            ),
        ]

        if not organisations:
            sections.append(
                self._render_empty_message(
                    "No organisations are currently published."
                )
            )

        return RenderedPage(
            title="Organisations",
            content=self._finalise_page(sections),
        )

    def render_toolboxes_page(self) -> RenderedPage:
        """Render the technical toolboxes page."""

        toolboxes = tuple(
            organisation
            for organisation in self.catalogue.published_organisations
            if organisation.type == "toolbox"
        )

        sections: list[str | None] = [
            heading("Technical Toolboxes"),
            paragraph(
                "Focused GitHub organisations containing projects, tools and "
                "resources for specific technical disciplines."
            ),
            self._render_organisation_summary(toolboxes),
            self._render_featured_organisations(
                include_types={"toolbox"},
                heading_text="Featured Toolboxes",
            ),
            self._render_organisation_entries(toolboxes),
        ]

        if not toolboxes:
            sections.append(
                self._render_empty_message(
                    "No technical toolboxes are currently published."
                )
            )

        return RenderedPage(
            title="Technical Toolboxes",
            content=self._finalise_page(sections),
        )

    def render_documentation_page(self) -> RenderedPage:
        """Render the documentation catalogue page."""

        documentation = self.catalogue.published_documentation

        sections: list[str | None] = [
            heading("Documentation"),
            paragraph(
                "A curated index of project documentation, shared references, "
                "standards, policies and technical guidance."
            ),
            self._render_documentation_summary(documentation),
            self._render_featured_documentation(),
            self._render_documentation_by_group(documentation),
        ]

        if not documentation:
            sections.append(
                self._render_empty_message(
                    "No documentation is currently published."
                )
            )

        return RenderedPage(
            title="Documentation",
            content=self._finalise_page(sections),
        )

    def render_all_pages(self) -> dict[str, RenderedPage]:
        """Render all configured portal catalogue pages."""

        return {
            "projects": self.render_projects_page(),
            "organisations": self.render_organisations_page(),
            "toolboxes": self.render_toolboxes_page(),
            "documentation": self.render_documentation_page(),
        }

    def _render_project_summary(
        self,
        projects: tuple[Project, ...],
    ) -> str | None:
        """Render project catalogue summary metadata."""

        if not projects:
            return None

        organisation_count = len(
            {project.organisation for project in projects}
        )

        category_count = len(
            {
                category_id
                for project in projects
                for category_id in project.categories
            }
        )

        return metadata_line(
            (
                badge("Projects", str(len(projects))),
                badge("Organisations", str(organisation_count)),
                badge("Categories", str(category_count)),
            )
        )

    def _render_organisation_summary(
        self,
        organisations: tuple[Organisation, ...],
    ) -> str | None:
        """Render organisation catalogue summary metadata."""

        if not organisations:
            return None

        category_count = len(
            {
                category_id
                for organisation in organisations
                for category_id in organisation.categories
            }
        )

        return metadata_line(
            (
                badge("Organisations", str(len(organisations))),
                badge("Categories", str(category_count)),
            )
        )

    def _render_documentation_summary(
        self,
        documentation: tuple[Documentation, ...],
    ) -> str | None:
        """Render documentation catalogue summary metadata."""

        if not documentation:
            return None

        type_count = len({entry.type for entry in documentation})

        category_count = len(
            {
                category_id
                for entry in documentation
                for category_id in entry.categories
            }
        )

        return metadata_line(
            (
                badge(
                    "Documentation Entries",
                    str(len(documentation)),
                ),
                badge("Types", str(type_count)),
                badge("Categories", str(category_count)),
            )
        )

    def _render_featured_projects(self) -> str | None:
        """Render featured project cards."""

        projects = self.catalogue.featured_projects

        if not projects:
            return None

        return join_sections(
            (
                heading("Featured Projects", level=2),
                self._render_project_entries(projects),
            )
        )

    def _render_featured_organisations(
        self,
        *,
        include_types: set[str] | None = None,
        exclude_types: set[str] | None = None,
        heading_text: str = "Featured Organisations",
    ) -> str | None:
        """Render featured organisation cards."""

        organisations = tuple(
            organisation
            for organisation in self.catalogue.featured_organisations
            if (
                include_types is None
                or organisation.type in include_types
            )
            and (
                exclude_types is None
                or organisation.type not in exclude_types
            )
        )

        if not organisations:
            return None

        return join_sections(
            (
                heading(heading_text, level=2),
                self._render_organisation_entries(organisations),
            )
        )

    def _render_featured_documentation(self) -> str | None:
        """Render featured documentation cards."""

        documentation = self.catalogue.featured_documentation

        if not documentation:
            return None

        return join_sections(
            (
                heading("Featured Documentation", level=2),
                self._render_documentation_entries(documentation),
            )
        )

    def _render_projects_by_organisation(
        self,
        projects: tuple[Project, ...],
    ) -> str | None:
        """Render projects grouped by their organisation."""

        if not projects:
            return None

        sections: list[str] = [
            heading("All Projects", level=2),
        ]

        grouped_projects: dict[str, list[Project]] = {}

        for project in projects:
            grouped_projects.setdefault(
                project.organisation,
                [],
            ).append(project)

        organisations = sorted(
            (
                organisation
                for organisation_id in grouped_projects
                if (
                    organisation
                    := self.catalogue.organisation_for(organisation_id)
                )
                is not None
            ),
            key=lambda organisation: (
                organisation.order,
                organisation.name.casefold(),
                organisation.id,
            ),
        )

        for organisation in organisations:
            organisation_projects = tuple(
                grouped_projects.get(organisation.id, [])
            )

            if not organisation_projects:
                continue

            sections.append(
                join_sections(
                    (
                        heading(organisation.name, level=3),
                        paragraph(organisation.description),
                        self._render_project_entries(
                            organisation_projects
                        ),
                    )
                )
            )

        orphaned_projects = tuple(
            project
            for project in projects
            if self.catalogue.organisation_for(
                project.organisation
            )
            is None
        )

        if orphaned_projects:
            sections.append(
                join_sections(
                    (
                        heading("Other Projects", level=3),
                        self._render_project_entries(
                            orphaned_projects
                        ),
                    )
                )
            )

        return join_sections(sections)

    def _render_organisations_by_group(
        self,
        organisations: tuple[Organisation, ...],
        *,
        excluded_group_ids: set[str] | None = None,
    ) -> str | None:
        """Render organisations grouped by configured type."""

        if not organisations:
            return None

        sections: list[str] = [
            heading("All Organisations", level=2),
        ]

        rendered_ids: set[str] = set()

        for group in self.configuration.organisation_groups:
            if (
                excluded_group_ids
                and group.id in excluded_group_ids
            ):
                continue

            group_organisations = tuple(
                organisation
                for organisation in organisations
                if organisation.type == group.id
            )

            if not group_organisations:
                if (
                    self.presentation.show_empty_sections
                    and group.description
                ):
                    sections.append(
                        join_sections(
                            (
                                heading(group.name, level=3),
                                paragraph(group.description),
                                self._render_empty_message(
                                    "No entries are currently published."
                                ),
                            )
                        )
                    )

                continue

            rendered_ids.update(
                organisation.id
                for organisation in group_organisations
            )

            sections.append(
                self._render_organisation_group(
                    group,
                    group_organisations,
                )
            )

        ungrouped = tuple(
            organisation
            for organisation in organisations
            if organisation.id not in rendered_ids
        )

        if ungrouped:
            sections.append(
                join_sections(
                    (
                        heading("Other Organisations", level=3),
                        self._render_organisation_entries(
                            ungrouped
                        ),
                    )
                )
            )

        return join_sections(sections)

    def _render_organisation_group(
        self,
        group: CatalogueGroup,
        organisations: tuple[Organisation, ...],
    ) -> str:
        """Render one configured organisation group."""

        return join_sections(
            (
                heading(group.name, level=3),
                paragraph(group.description),
                self._render_organisation_entries(organisations),
            )
        )

    def _render_documentation_by_group(
        self,
        documentation: tuple[Documentation, ...],
    ) -> str | None:
        """Render documentation grouped by configured type."""

        if not documentation:
            return None

        sections: list[str] = [
            heading("All Documentation", level=2),
        ]

        rendered_ids: set[str] = set()

        for group in self.configuration.documentation_groups:
            group_entries = tuple(
                entry
                for entry in documentation
                if entry.type == group.id
            )

            if not group_entries:
                if self.presentation.show_empty_sections:
                    sections.append(
                        join_sections(
                            (
                                heading(group.name, level=3),
                                paragraph(group.description),
                                self._render_empty_message(
                                    "No entries are currently published."
                                ),
                            )
                        )
                    )

                continue

            rendered_ids.update(entry.id for entry in group_entries)

            sections.append(
                join_sections(
                    (
                        heading(group.name, level=3),
                        paragraph(group.description),
                        self._render_documentation_entries(
                            group_entries
                        ),
                    )
                )
            )

        ungrouped = tuple(
            entry
            for entry in documentation
            if entry.id not in rendered_ids
        )

        if ungrouped:
            sections.append(
                join_sections(
                    (
                        heading("Other Documentation", level=3),
                        self._render_documentation_entries(
                            ungrouped
                        ),
                    )
                )
            )

        return join_sections(sections)

    def _render_project_entries(
        self,
        projects: Iterable[Project],
    ) -> str | None:
        """Render a sequence of project cards."""

        entries = tuple(projects)

        if not entries:
            return None

        return self._render_card_grid(
            self._render_project_card(project)
            for project in entries
        )

    def _render_organisation_entries(
        self,
        organisations: Iterable[Organisation],
    ) -> str | None:
        """Render a sequence of organisation cards."""

        entries = tuple(organisations)

        if not entries:
            return None

        return self._render_card_grid(
            self._render_organisation_card(organisation)
            for organisation in entries
        )

    def _render_documentation_entries(
        self,
        documentation: Iterable[Documentation],
    ) -> str | None:
        """Render a sequence of documentation cards."""

        entries = tuple(documentation)

        if not entries:
            return None

        return self._render_card_grid(
            self._render_documentation_card(entry)
            for entry in entries
        )

    def _render_project_card(self, project: Project) -> str:
        """Render one project card."""

        organisation = self.catalogue.organisation_for(
            project.organisation
        )

        context_items: list[str] = []

        if organisation:
            context_items.append(
                f":material-domain: {organisation.name}"
            )

        if self.presentation.show_status and project.status:
            context_items.append(
                f":material-pulse: {project.status.title()}"
            )

        if self.presentation.show_maturity and project.maturity:
            context_items.append(
                f":material-chart-timeline-variant: "
                f"{project.maturity.title()}"
            )

        technologies: str | None = None

        if (
            self.presentation.show_technologies
            and project.technologies
        ):
            technologies = self._render_tags(project.technologies)

        categories = self._render_categories(project.categories)

        return self._render_card(
            icon="material-source-repository",
            title=project.name,
            description=project.description,
            context=context_items,
            tags=technologies,
            categories=categories,
            links=self._render_action_links(
                self._filter_project_links(project)
            ),
        )

    def _render_organisation_card(
        self,
        organisation: Organisation,
    ) -> str:
        """Render one organisation card."""

        context_items = [
            (
                ":material-github: "
                f"{inline_code(organisation.github_organisation)}"
            )
        ]

        projects = self.catalogue.projects_for_organisation(
            organisation.id
        )

        if projects:
            project_label = (
                "project"
                if len(projects) == 1
                else "projects"
            )

            context_items.append(
                f":material-package-variant-closed: "
                f"{len(projects)} published {project_label}"
            )

        categories = self._render_categories(
            organisation.categories
        )

        return self._render_card(
            icon="material-domain",
            title=organisation.name,
            description=organisation.description,
            context=context_items,
            categories=categories,
            links=self._render_action_links(
                organisation.links
            ),
        )

    def _render_documentation_card(
        self,
        documentation: Documentation,
    ) -> str:
        """Render one documentation card."""

        context_items = [
            (
                ":material-file-document-outline: "
                f"{self._documentation_type_name(documentation.type)}"
            )
        ]

        organisation = self.catalogue.organisation_for(
            documentation.organisation
        )

        if organisation:
            context_items.append(
                f":material-domain: {organisation.name}"
            )

        project = self.catalogue.project_for(
            documentation.project
        )

        if project:
            context_items.append(
                f":material-source-repository: {project.name}"
            )

        categories = self._render_categories(
            documentation.categories
        )

        return self._render_card(
            icon="material-book-open-page-variant",
            title=documentation.name,
            description=documentation.description,
            context=context_items,
            categories=categories,
            links=self._render_action_links(
                self._filter_documentation_links(documentation)
            ),
        )

    def _render_card(
        self,
        *,
        icon: str,
        title: str,
        description: str,
        context: Iterable[str] = (),
        tags: str | None = None,
        categories: str | None = None,
        links: str | None = None,
    ) -> str:
        """Render one Material for MkDocs catalogue card."""

        sections: list[str] = [
            f":{icon}:{{ .lg .middle }} __{title}__",
            "---",
            paragraph(description),
        ]

        context_items = tuple(
            item
            for item in context
            if item
        )

        if context_items:
            sections.append(
                "  \n".join(context_items)
            )

        if tags:
            sections.append(tags)

        if categories:
            sections.append(categories)

        if links:
            sections.extend(
                (
                    "---",
                    links,
                )
            )

        return join_sections(sections)

    def _render_card_grid(
        self,
        cards: Iterable[str],
    ) -> str | None:
        """Render cards inside a constrained Material grid."""

        card_items = tuple(
            card
            for card in cards
            if card
        )

        if not card_items:
            return None

        rendered_cards = "\n\n".join(
            self._indent_card(card)
            for card in card_items
        )

        return (
            '<div class="grid cards catalogue-grid" markdown>\n\n'
            f"{rendered_cards}\n\n"
            "</div>"
        )

    def _indent_card(self, card: str) -> str:
        """Indent card content beneath a Markdown list item."""

        lines = card.splitlines()

        if not lines:
            return "-"

        rendered_lines = [
            f"-   {lines[0]}",
        ]

        for line in lines[1:]:
            if line:
                rendered_lines.append(f"    {line}")
            else:
                rendered_lines.append("")

        return "\n".join(rendered_lines)

    def _render_tags(
        self,
        values: Iterable[str],
    ) -> str | None:
        """Render a compact sequence of technology tags."""

        items = tuple(
            value
            for value in values
            if value
        )

        if not items:
            return None

        return " ".join(
            inline_code(value)
            for value in items
        )

    def _render_categories(
        self,
        category_ids: Iterable[str],
    ) -> str | None:
        """Render compact category links for a catalogue entry."""

        if not self.presentation.show_categories:
            return None

        categories = self.catalogue.categories_for(category_ids)

        if not categories:
            return None

        return " ".join(
            (
                f'<span class="catalogue-category">'
                f"{category.display_name}"
                "</span>"
        )
            for category in categories
        )

    def _render_action_links(
        self,
        links: Iterable[Any],
    ) -> str | None:
        """Render card actions using consistent icons."""

        rendered_links: list[str] = []

        for index, link in enumerate(links):
            icon = self._link_icon(link.label)

            if index == 0:
                css_class = "catalogue-action card-primary-link"
            else:
                css_class = "catalogue-action"

            rendered_links.append(
                f"[:{icon}: {link.label}]({link.url})"
                f"{{ .{css_class.replace(' ', ' .')} }}"
            )

        if not rendered_links:
            return None

        return " ".join(rendered_links)

    def _link_icon(self, label: str) -> str:
        """Return a Material icon name for a link label."""

        normalised = label.casefold()

        if "documentation" in normalised or "read" in normalised:
            return "material-book-open-page-variant"

        if "repository" in normalised or "github" in normalised:
            return "material-github"

        if "website" in normalised or "site" in normalised:
            return "material-web"

        if "download" in normalised:
            return "material-download"

        return "material-arrow-top-right"

    def _filter_project_links(
        self,
        project: Project,
    ) -> tuple[Any, ...]:
        """Return project links permitted by presentation settings."""

        return tuple(
            link
            for link in project.links
            if (
                link.label != "Repository"
                or self.presentation.show_repository_links
            )
            and (
                link.label != "Documentation"
                or self.presentation.show_documentation_links
            )
        )

    def _filter_documentation_links(
        self,
        documentation: Documentation,
    ) -> tuple[Any, ...]:
        """Return documentation links permitted by presentation settings."""

        return tuple(
            link
            for link in documentation.links
            if (
                link.label != "Source Repository"
                or self.presentation.show_repository_links
            )
            and (
                link.label != "Read Documentation"
                or self.presentation.show_documentation_links
            )
        )

    def _documentation_type_name(
        self,
        type_id: str,
    ) -> str:
        """Resolve a documentation type identifier to its display name."""

        for group in self.configuration.documentation_groups:
            if group.id == type_id:
                return group.name

        return type_id.replace("-", " ").title()

    def _render_empty_message(self, message: str) -> str:
        """Render a consistent empty-section message."""

        return f"*{message}*"

    def _finalise_page(
        self,
        sections: Iterable[str | None],
    ) -> str:
        """Join page sections and ensure a trailing newline."""

        content = join_sections(sections)

        front_matter = """---
hide:
  - navigation
  - toc
---"""

        return f"{front_matter}\n\n{content}\n"
