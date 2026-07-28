---
hide:
  - navigation
  - toc
---

{{ filter_panel(
    "policy",
    compact=True,
    search_label="Search policies",
    search_placeholder="Search by policy name or description",
    summary_text="Showing all policies",
) }}

{{ catalogue_grid("policy", "policy") }}

{{ catalogue_empty(
    "policy",
    "No matching policies",
    "Try changing the search text, selecting a different category or clearing the filters.",
) }}
