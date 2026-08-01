---
hide:
  - navigation
  - toc
banner_expiry_days: 28
---

{{ filter_panel(
    "project",
    search_label="Search projects",
    search_placeholder="Search by project name, description, or category...",
    summary_text="Showing…",
    include_organisation=True,
    include_status=True,
    include_sort=True,
) }}

{{ catalogue_grid("project", "project", banner_expiry_days=page.meta.banner_expiry_days or 28) }}

{{ catalogue_empty(
    "project",
    "No matching projects",
    "Try changing the search text or selecting different filters.",
) }}
