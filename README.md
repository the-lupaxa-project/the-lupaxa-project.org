# Lupaxa Project Website

The website provides a consistent look and feel, reusable styling, common
components and sensible defaults for search engines, social media and modern
browsers.

## Features

- Responsive Material for MkDocs layout
- Custom Lupaxa styling
- Reusable page templates
- Automatic Open Graph metadata
- Twitter / X Cards
- Canonical URLs
- Social preview images
- Custom navigation components
- Configurable branding
- Consistent documentation standards

## Site-wide Configuration

The following settings are configured in `mkdocs.yml`.

### Basic Metadata

```yaml
site_name: The Lupaxa Project

site_description: >-
  Open source software, reusable workflows, documentation and developer
  tooling from The Lupaxa Project.

site_author: The Lupaxa Project

site_url: https://www.thelupaxaproject.org/
```

These values provide the default metadata for the website and are also used for
social media previews unless overridden by an individual page.

### Social Media Configuration

```yaml
extra:
  theme_color: "#203959"

  social_image: assets/images/social-card.png
  social_image_width: 1200
  social_image_height: 630

  social_locale: en_GB
  twitter_card: summary_large_image
```

#### `theme_color`

Sets the browser theme colour used by supported browsers and mobile devices.

Example:

```yaml
theme_color: "#203959"
```

#### `social_image`

Specifies the default social preview image used by the entire website.

Example:

```yaml
social_image: assets/images/social-card.png
```

The recommended image size is:

- PNG format
- 1200 × 630 pixels
- Landscape orientation
- Less than approximately 1 MB

#### `social_image_width`

Advertises the width of the social preview image.

Normally:

```yaml
social_image_width: 1200
```

#### `social_image_height`

Advertises the height of the social preview image.

Normally:

```yaml
social_image_height: 630
```

#### `social_locale`

Sets the Open Graph locale.

Example:

```yaml
social_locale: en_GB
```

#### `twitter_card`

Sets the Twitter / X card type.

Normally:

```yaml
twitter_card: summary_large_image
```

## Page Metadata

Individual pages can override the site defaults using YAML front matter.

Example:

```markdown
---
description: Browse every project published by The Lupaxa Project.

social_title: Projects

social_image: assets/images/social/projects.png
---

# Projects
```

### Supported Page Metadata

#### `description`

Overrides the default site description.

Example:

```yaml
description: Browse every project published by The Lupaxa Project.
```

#### `social_title`

Overrides the title used for Open Graph and Twitter cards.

Example:

```yaml
social_title: Projects
```

If omitted, the template automatically generates:

```text
<Page Title> | <Site Name>
```

#### `social_image`

Overrides the default social preview image for a single page.

Example:

```yaml
social_image: assets/images/social/projects.png
```

## Metadata Priority

The template uses the following precedence.

| Metadata     | Page Override  | Site Default         |
| :----------- | :------------- | :------------------- |
| Title        | `social_title` | `site_name`          |
| Description  | `description`  | `site_description`   |
| Social Image | `social_image` | `extra.social_image` |

## Supported Social Platforms

The generated metadata is compatible with:

- Facebook
- LinkedIn
- Discord
- Slack
- Microsoft Teams
- WhatsApp
- X (Twitter)
- iMessage
- Most applications that support the Open Graph protocol

## File Locations

```text
overrides/
    main.html

mkdocs.yml

mkdocs/
└── assets/
    └── images/
        └── social-card.png
```

`main.html` automatically generates the required Open Graph and Twitter / X
metadata using the values defined in `mkdocs.yml` together with any page
metadata supplied in YAML front matter.
