"""MkDocs macros for catalogue pages.

Loads YAML catalogue data and exposes Jinja macros that emit the same
HTML/Markdown structure previously hand-authored in the page files.
"""

from __future__ import annotations

import html
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from banner_lib import (
    BANNER_PRESETS,
    BANNER_TONES,
    DEFAULT_BANNER_EXPIRY_DAYS,
    POLICY_BANNER_PRESETS,
    PROJECT_BANNER_PRESETS,
    banner_markup as _shared_banner_markup,
    parse_iso_date,
    resolve_banner as _shared_resolve_banner,
)
from quotes_lib import (
    collect_tags as collect_quote_tags,
    load_quotes_data,
    published_quotes,
    validate_quotes,
)
from gallery_lib import (
    collect_tags as collect_gallery_tags,
    is_remote_media,
    load_gallery_data,
    published_entries,
    validate_gallery,
)

DATA_DIR = ROOT / "data"

# Shared brand mark for policy cards (same visual slot as project/org logos).
DEFAULT_POLICY_LOGO = (
    "https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/"
    "master/logos/organisations/the-lupaxa-project/readme-logo-128.png"
)
DEFAULT_POLICY_LOGO_ALT = "The Lupaxa Project"


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
        f'    <button type="button" class="catalogue-category">{category}</button>'
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


def _resolve_banner(raw: Any) -> tuple[str, str, str] | None:
    """Return (label, tone, filter_key) for a project banner, or None."""
    return _shared_resolve_banner(raw)


def _banner_markup(raw: Any) -> str:
    return _shared_banner_markup(raw)


def define_env(env):
    def _published(items: list[dict]) -> list[dict]:
        return [item for item in items if item.get("published", True)]

    organisations = _published(_load_yaml("organisations.yml"))
    projects = _published(_load_yaml("projects.yml"))
    policies = _published(_load_yaml("policies.yml"))

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
        include_status: bool = False,
        status_kind: str = "project",
        category_label: str = "Category",
        organisation_label: str = "Organisation",
        status_label: str = "Status",
        clear_label: str = "Clear filters",
    ) -> str:
        classes = "filter-panel filter-panel--compact" if compact else "filter-panel"
        organisation_block = ""
        if include_organisation:
            organisation_block = f"""
    <div class="filter-panel-select">
        <label for="{prefix}-organisation">{organisation_label}</label>
        <select id="{prefix}-organisation" data-{prefix}-organisation>
            <option value="">All Organisations</option>
        </select>
    </div>"""
        status_block = ""
        if include_status:
            # Fixed lifecycle list (not derived from cards on the page).
            if status_kind == "project":
                presets = PROJECT_BANNER_PRESETS
                show_stable = True
            elif status_kind == "policy":
                presets = POLICY_BANNER_PRESETS
                show_stable = False
            else:
                raise ValueError(f"Unrecognised status_kind: {status_kind!r}")

            if status_kind == "policy":
                # Segmented All | New | Updated (same pattern as articles).
                toggle_buttons = [
                    ("all", "All"),
                    ("new", "New"),
                    ("updated", "Updated"),
                ]
                options_markup = "\n".join(
                    f"""            <button
                type="button"
                class="filter-panel-toggle__option"
                data-{prefix}-status="{html.escape(slug, quote=True)}"
                aria-pressed="{"true" if slug == "all" else "false"}"
            >
                {html.escape(label)}
            </button>"""
                    for slug, label in toggle_buttons
                )
                status_block = f"""
    <div class="filter-panel-toggle" role="group" aria-labelledby="{prefix}-status-label">
        <label id="{prefix}-status-label">{status_label}</label>
        <div class="filter-panel-toggle__options">
{options_markup}
        </div>
    </div>"""
            else:
                status_options = "\n".join(
                    f'            <option value="{html.escape(slug, quote=True)}">'
                    f"{html.escape(label)}</option>"
                    for slug, (label, _) in presets.items()
                )
                stable_option = (
                    '\n            <option value="stable">Stable</option>'
                    if show_stable
                    else ""
                )
                status_block = f"""
    <div class="filter-panel-select">
        <label for="{prefix}-status">{status_label}</label>
        <select id="{prefix}-status" data-{prefix}-status>
            <option value="">All Statuses</option>
{status_options}{stable_option}
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
            <option value="">All Categories</option>
        </select>
    </div>{status_block}
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

    def project_card(
        item: dict, *, expiry_days: int = DEFAULT_BANNER_EXPIRY_DAYS
    ) -> str:
        categories = _categories_markup(item["categories"])
        description = _indent(item["description"])
        banner = _shared_banner_markup(
            item.get("banner"),
            presets=PROJECT_BANNER_PRESETS,
            event_date=parse_iso_date(item.get("released_date")),
            expiry_days=expiry_days,
            time_limited_statuses=frozenset({"released"}),
        )
        banner_block = f"{banner}\n\n" if banner else ""
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

{banner_block}    <img
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

    def policy_card(
        item: dict, *, expiry_days: int = DEFAULT_BANNER_EXPIRY_DAYS
    ) -> str:
        categories = _categories_markup(item["categories"])
        description = _indent(item["description"])
        raw_banner = item.get("banner")
        resolved = _shared_resolve_banner(raw_banner, presets=POLICY_BANNER_PRESETS)
        event_date = None
        if resolved:
            filter_key = resolved[2]
            date_field = "updated_date" if filter_key == "updated" else "publish_date"
            event_date = parse_iso_date(item.get(date_field))
        banner = _shared_banner_markup(
            raw_banner,
            presets=POLICY_BANNER_PRESETS,
            event_date=event_date,
            expiry_days=expiry_days,
            time_limited_statuses=frozenset({"new", "updated"}),
        )
        banner_block = f"{banner}\n\n" if banner else ""
        logo = html.escape(item.get("logo", DEFAULT_POLICY_LOGO), quote=True)
        logo_alt = html.escape(
            item.get("logo_alt", DEFAULT_POLICY_LOGO_ALT), quote=True
        )
        action = _action_link(
            "repository",
            item["document"],
            "View on GitHub",
            "material-github",
        )
        return f"""
-   :{item["icon"]}:{{ .lg .middle }} **{item["name"]}**

    ---

{banner_block}    <img
        class="catalogue-logo"
        title="{logo_alt}"
        src="{logo}"
        alt="{logo_alt}"
    />

{description}

{categories}

    ---

{action}
""".strip()

    @env.macro
    def catalogue_grid(
        prefix: str,
        kind: str,
        banner_expiry_days: int = DEFAULT_BANNER_EXPIRY_DAYS,
    ) -> str:
        if kind == "organisation":
            cards = "\n\n".join(organisation_card(item) for item in organisations)
        elif kind == "project":
            cards = "\n\n".join(
                project_card(item, expiry_days=banner_expiry_days)
                for item in projects
            )
        elif kind == "policy":
            cards = "\n\n".join(
                policy_card(item, expiry_days=banner_expiry_days)
                for item in policies
            )
        else:
            raise ValueError(f"Unknown catalogue kind: {kind}")

        return f"""
<div class="grid cards catalogue-grid" data-{prefix}-catalogue markdown>

{cards}

</div>
""".strip()


    quotes_path = Path(env.project_dir) / "data" / "quotes.yml"

    def validated_quotes():
        data = load_quotes_data(quotes_path)
        validate_quotes(data)
        return data

    @env.macro
    def quotes_data():
        return validated_quotes()

    @env.macro
    def wall_quotes():
        return published_quotes(validated_quotes())

    @env.macro
    def wall_tags():
        return collect_quote_tags(published_quotes(validated_quotes()))

    gallery_path = Path(env.project_dir) / "data" / "gallery.yml"

    def validated_gallery():
        data = load_gallery_data(gallery_path)
        validate_gallery(data)
        return data

    @env.macro
    def gallery_data():
        return validated_gallery()

    @env.macro
    def wall_gallery_entries():
        return published_entries(validated_gallery())

    @env.macro
    def gallery_wall_tags():
        return collect_gallery_tags(published_entries(validated_gallery()))

    @env.macro
    def gallery_media_is_remote(path: str) -> bool:
        return is_remote_media(path)

    @env.macro
    def featured_projects(banner_expiry_days: int = DEFAULT_BANNER_EXPIRY_DAYS) -> str:
        featured = [item for item in projects if item.get("featured")]
        cards = "\n\n".join(
            project_card(item, expiry_days=banner_expiry_days) for item in featured
        )
        return f"""
<div class="grid cards catalogue-grid" markdown>

{cards}

</div>
""".strip()
