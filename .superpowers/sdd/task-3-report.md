# Task 3 Report: Gallery Page

## Status

Implemented the portal-native Gallery page, stylesheet, lifecycle-aware JavaScript,
and Gallery registrations in `mkdocs.yml`.

## Delivered

- `mkdocs/gallery.md` renders tag/media filters, photo/video masonry cards, and
  the accessible lightbox using `photos_data()`, `wall_photos()`, and
  `photo_wall_tags()`.
- `mkdocs/assets/stylesheets/50-pages/gallery.css` adapts the R&D masonry and
  lightbox styles to portal tokens without suppressing Material chrome or
  overriding the page background.
- `mkdocs/assets/javascript/gallery.js` implements filtering, shuffled layouts,
  masonry relayouts, lightbox navigation, keyboard focus trapping, and Material
  instant-navigation initialization.
- The Gallery JavaScript uses a single persistent resize listener and a single
  persistent document keyboard listener, both routed to the active Gallery DOM
  after instant navigation.
- `mkdocs.yml` contains Gallery nav, CSS, and JavaScript registrations after
  the existing Quotes entries in the working tree.

## Verification

`mkdocs build --strict` exited successfully. The generated
`site/gallery/index.html` exists and contains both `gallery-wall` and
`gallery-lightbox`.

The edited task files have no IDE linter diagnostics.

## Self-review

- Verified no R&D Material chrome-hiding selectors, full-page background
  overrides, inline root styles, or title-setting scripts were copied.
- Verified Gallery uses the required `photo_wall_tags()` macro.
- Verified masonry constants remain 280px card width and 16px gap in JavaScript,
  matching the stylesheet variables.

## Commit concern

`mkdocs.yml` also contains unrelated Articles and Quotes work. To avoid
committing that WIP, its Gallery registrations remain unstaged in the working
tree. The three Gallery-only files were committed independently in
`8db0bfd Add portal-native Gallery page after Quotes.`

## Follow-up fix

- `initGalleryWall()` now destroys the previous lightbox before it queries for
  Gallery DOM. This releases `body.lightbox-open`, clears the previous wall's
  inert state, and stops/resets any lightbox video on both Gallery re-init and
  navigation to a page without masonry.

## Follow-up verification

- A focused Node assertion verified cleanup is invoked before the masonry
  lookup and that it destroys the active lightbox state.
- `mkdocs build --strict` exited successfully (the build reported only its
  existing informational warnings about unlisted Articles pages).
