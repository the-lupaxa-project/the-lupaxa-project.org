# The Lupaxa Project Portal CSS Split

This package contains the current portal stylesheet split into logical files.

## Installation

Copy the contents into:

```text
mkdocs/assets/stylesheets/
```

Then replace the existing `extra_css` block in `mkdocs.yml` with the contents of:

```text
mkdocs-extra-css.yml
```

Do not keep the old monolithic stylesheet loaded at the same time, otherwise
the rules will be duplicated.

The split is intended to preserve the current styling while making future
changes easier to isolate.
