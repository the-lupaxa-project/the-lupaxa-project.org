---
hide:
  - navigation
  - toc
banner_expiry_days: 28
---

{{ filter_panel(
    "policy",
    compact=True,
    search_label="Search policies",
    search_placeholder="Search by policy name or description",
    summary_text="Showing…",
) }}

{{ catalogue_grid("policy", "policy", banner_expiry_days=page.meta.banner_expiry_days or 28) }}

{{ catalogue_empty(
    "policy",
    "No matching policies",
    "Try changing the search text, selecting a different category or clearing the filters.",
) }}
