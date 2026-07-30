---
hide:
  - navigation
  - toc
---

{{ filter_panel(
    "project",
    search_label="Search projects",
    search_placeholder="Search by project name, description, or category...",
    summary_text="Showing all projects",
    include_organisation=True,
    include_status=True,
) }}

{{ catalogue_grid("project", "project") }}

{{ catalogue_empty(
    "project",
    "No matching projects",
    "Try changing the search text or selecting different filters.",
) }}
