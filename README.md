<p align="center">
    <a href="https://github.com/the-lupaxa-project">
        <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/the-lupaxa-project/readme-logo.png" alt="Organisation Logo" />
    </a>
</p>

<h1 align="center">The Lupaxa Project portal</h1>

Central MkDocs Material site for organisations, projects, and policies across
The Lupaxa Project ecosystem.

Published at <https://thelupaxaproject.org/>.

## Prerequisites

- Python 3.13+
- Node.js 22+ (only required for markdownlint)
- `yamllint` (optional; `python -m pip install yamllint`)

## Local development

```bash
make init
make install-dev
make mkdocs-serve
```

Or without Make:

```bash
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Open the URL printed by MkDocs (usually `http://127.0.0.1:8000/`).

`mkdocs.yml` watches `data/`, `hooks/`, and every build-time Python module
(`main.py`, `*_lib.py`), so catalogue YAML and macro edits reload
automatically while `mkdocs serve` is running. Add new build scripts to
`watch` when you create them — MkDocs does not support globs there.

Strict production build:

```bash
python -m mkdocs build --strict
```

Markdown lint:

```bash
npx markdownlint-cli "mkdocs/**/*.md" --config .markdownlint.yml
```

YAML lint:

```bash
yamllint -c .yamllint.yml .github data mkdocs.yml .markdownlint.yml .yamllint.yml
```

## Catalogue content

Catalogue entries live in YAML under `data/`:

| File | Page |
| --- | --- |
| `data/organisations.yml` | Organisations |
| `data/quotes.yml` | Quotes masonry wall |
| `data/gallery.yml` | Gallery masonry wall (`page.show_count: all` or a number; `page.show_media_filters: true` for images/videos filters) |
| `data/projects.yml` | Projects (home shows nine newest by `publish_date`; six on tablet/mobile) |
| `data/policies.yml` | Policies |

`main.py` loads that data for `mkdocs-macros-plugin`. Pages call macros such as
`filter_panel`, `catalogue_grid`, and `newest_projects` so card markup stays
in one place.

Brand logos remain remote URLs from the `brand-assets` repository.

## Layout overview

```text
data/                     Catalogue YAML
main.py                   Macros plugin entry
mkdocs/                   Page Markdown and static assets
overrides/                Material theme overrides
requirements.txt          Pinned MkDocs dependencies
.github/workflows/        Publish + PR validate
```

CSS is numbered by cascade layer under `mkdocs/assets/stylesheets/`.
JavaScript is split under `mkdocs/assets/javascript/`:

- `page-lifecycle.js` — load + Material instant navigation helpers (`onPageRender`)
- `header-active-nav.js` — header active state
- `catalogue-filters.js` — catalogue search / filter / URL sync
- `masonry-wall.js` — shared masonry layout and text filters
- `quotes.js` — quotes wall (uses masonry-wall)
- `gallery.js` — gallery wall + lightbox (uses masonry-wall)

## Page social metadata

Site-wide defaults are set in `mkdocs.yml` under `extra`:

```yaml
extra:
  generator: false
  social_image: assets/images/social-media/social-card.png
  social_image_width: 1200
  social_image_height: 630
  social_logo: >-
    https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/organisations/the-lupaxa-project/readme-logo.png
  social_locale: en_GB
  theme_color: "#203959"
  twitter_card: summary_large_image
```

Optional per-page overrides in front matter:

```yaml
---
description: Short page description for search and social cards.
social_title: Custom social title
social_image: assets/images/social-media/social-card.png
---
```

`overrides/main.html` omits image meta tags when no social image path is set.

## Publishing

Push to `master` triggers `.github/workflows/publish-mkdocs.yml`, which calls
the org reusable MkDocs publisher. That workflow installs from
`requirements.txt` when the file is present.

Pull requests run `.github/workflows/validate-mkdocs.yml`, which calls the org
reusable MkDocs site validator (`mkdocs build --strict` + optional markdownlint).

> Note: both the reusable publisher (conditional `requirements.txt`) and the
> reusable validator must be merged in `the-lupaxa-project/workflows` before
> GitHub Actions can use them from `@master`.

<a href="https://github.com/the-lupaxa-project">
    <img src="https://raw.githubusercontent.com/the-lupaxa-project/brand-assets/master/logos/components/footer.svg" alt="The Lupaxa Project Footer" width="100%" />
</a>
