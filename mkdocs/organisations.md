---
hide:
  - navigation
  - toc
---

{{ filter_panel(
    "organisation",
    compact=True,
    search_label="Search organisations",
    search_placeholder="Search by organisation name",
    summary_text="Showing all organisations",
) }}

{{ catalogue_grid("organisation", "organisation") }}

{{ catalogue_empty(
    "organisation",
    "No matching organisations",
    "Try changing the search text, selecting a different category or clearing the filters.",
) }}
