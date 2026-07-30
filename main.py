"""MkDocs macros for catalogue pages.

Loads YAML catalogue data and exposes Jinja macros that emit the same
HTML/Markdown structure previously hand-authored in the page files.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from gallery_lib import (
    collect_tags as collect_photo_tags,
    load_photos_data,
    published_photos,
    validate_photos,
)

DATA_DIR = ROOT / "data"


def _load_yaml(name: str) -> list[dict]:
    path = DATA_DIR / name
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or []
    if not isinstance(data, list):
        raise TypeError(f"{path} must contain a YAML list")
    return data


def _indent(text: str, prefix: str = "    ") -> str:
    return "\n".join(
        f"{prefix}{line}" if line else prefix.rstrip()
        for line in text.strip().splitlines()
    )


def _categories_markup(categories: list[str]) -> str:
    return "\n".join(
        f'    <span class="catalogue-category">{category}</span>'
        for category in categories
    )


def _organisation_logo_title(name: str) -> str:
    if name.startswith("The "):
        return f"View projects in {name}"
    return f"View projects in the {name}"


def _action_link(modifier: str, href: str, label: str, icon: str) -> str:
    return (
        f'    <a\n'
        f'        class="catalogue-action catalogue-action--{modifier}"\n'
        f'        href="{href}"\n'
        f'        target="_blank"\n'
        f'        rel="noopener noreferrer">\n'
        f'        <span class="md-icon">:{icon}:</span>\n'
        f'        {label}\n'
        f'    </a>'
    )


def define_env(env):
    organisations = _load_yaml("organisations.yml")
    projects = _load_yaml("projects.yml")
    policies = _load_yaml("policies.yml")

    env.variables["catalogue_organisations"] = organisations
    env.variables["catalogue_projects"] = projects
    env.variables["catalogue_policies"] = policies

    @env.macro
    def filter_panel(
        prefix: str,
        *,
        compact: bool = False,
        search_label: str,
        search_placeholder: str,
        summary_text: str,
        include_organisation: bool = False,
        category_label: str = "Category",
        organisation_label: str = "Organisation",
        clear_label: str = "Clear filters",
    ) -> str:
        classes = "filter-panel filter-panel--compact" if compact else "filter-panel"
        organisation_block = ""
        if include_organisation:
            organisation_block = f"""
    <div class="filter-panel-select">
        <label for="{prefix}-organisation">{organisation_label}</label>
        <select id="{prefix}-organisation" data-{prefix}-organisation>
            <option value="">All organisations</option>
        </select>
    </div>"""

        return f"""
<div class="{classes}" data-{prefix}-filters>
    <div class="filter-panel-search">
        <label for="{prefix}-search">{search_label}</label>
        <input
            id="{prefix}-search"
            type="search"
            placeholder="{search_placeholder}"
            autocomplete="off"
            data-{prefix}-search
        />
    </div>{organisation_block}
    <div class="filter-panel-select">
        <label for="{prefix}-category">{category_label}</label>
        <select id="{prefix}-category" data-{prefix}-category>
            <option value="">All categories</option>
        </select>
    </div>
    <div class="filter-panel-actions">
        <button
            type="button"
            class="md-button lupaxa-button filter-panel-clear"
            data-{prefix}-clear
        >
            {clear_label}
        </button>
    </div>
    <div
        class="filter-panel-summary"
        aria-live="polite"
        data-{prefix}-summary
    >
        {summary_text}
    </div>
</div>
""".strip()

    @env.macro
    def catalogue_empty(prefix: str, heading: str, hint: str) -> str:
        return f"""
<div class="catalogue-empty-state" data-{prefix}-empty hidden markdown>

:material-filter-off:{{ .lg }}

**{heading}**

{hint}

</div>
""".strip()

    def organisation_card(item: dict) -> str:
        categories = _categories_markup(item["categories"])
        description = _indent(item["description"])
        title = _organisation_logo_title(item["name"])
        action = _action_link(
            "repository",
            item["repository"],
            "View on GitHub",
            "material-github",
        )
        return f"""
-   :{item["icon"]}:{{ .lg .middle }} **{item["name"]}**

    ---

    <img
        class="catalogue-logo"
        title="{title}"
        data-organisation="{item["name"]}"
        src="{item["logo"]}"
        alt="{item.get("logo_alt", item["name"])}"
    />

{description}

{categories}

    ---

{action}
""".strip()

    def project_card(item: dict) -> str:
        categories = _categories_markup(item["categories"])
        description = _indent(item["description"])
        actions = [
            _action_link(
                "repository",
                item["repository"],
                "View on GitHub",
                "material-github",
            )
        ]
        documentation = item.get("documentation")
        if documentation:
            actions.append(
                _action_link(
                    "documentation",
                    documentation,
                    "Documentation",
                    "material-book-open-page-variant",
                )
            )
        actions_markup = "\n".join(actions)
        return f"""
-   :{item["icon"]}:{{ .lg .middle }} **{item["name"]}**

    ---

    <img
        class="catalogue-logo"
        title="{item["organisation"]}"
        data-organisation="{item["organisation"]}"
        src="{item["logo"]}"
        alt="{item.get("logo_alt", item["organisation"])}"
    />

{description}

{categories}

    ---

{actions_markup}
""".strip()

    def policy_card(item: dict) -> str:
        categories = _categories_markup(item["categories"])
        description = _indent(item["description"])
        action = _action_link(
            "repository",
            item["document"],
            "View on GitHub",
            "material-github",
        )
        return f"""
-   :{item["icon"]}:{{ .lg .middle }} **{item["name"]}**

    ---

{description}

{categories}

    ---

{action}
""".strip()

    @env.macro
    def catalogue_grid(prefix: str, kind: str) -> str:
        if kind == "organisation":
            cards = "\n\n".join(organisation_card(item) for item in organisations)
        elif kind == "project":
            cards = "\n\n".join(project_card(item) for item in projects)
        elif kind == "policy":
            cards = "\n\n".join(policy_card(item) for item in policies)
        else:
            raise ValueError(f"Unknown catalogue kind: {kind}")

        return f"""
<div class="grid cards catalogue-grid" data-{prefix}-catalogue markdown>

{cards}

</div>
""".strip()

    photos_path = Path(env.project_dir) / "data" / "photos.yml"

    def validated_photos():
        data = load_photos_data(photos_path)
        validate_photos(data)
        return data

    @env.macro
    def photos_data():
        return validated_photos()

    @env.macro
    def wall_photos():
        return published_photos(validated_photos())

    @env.macro
    def photo_wall_tags():
        return collect_photo_tags(published_photos(validated_photos()))

    @env.macro
    def featured_projects() -> str:
        featured = [item for item in projects if item.get("featured")]
        cards = "\n\n".join(project_card(item) for item in featured)
        return f"""
<div class="grid cards catalogue-grid" markdown>

{cards}

</div>
""".strip()
