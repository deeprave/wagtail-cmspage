## Purpose

Provides the CMS `{% render_image %}` tag that emits a WebP `<picture>` pair from sized renditions, without repeating identical rendition lookups on one page render.

## ADDED Requirements

### Requirement: Picture markup uses sized renditions

The system SHALL render `{% render_image %}` as a WebP `<source>` plus an `<img>` whose `src` is the fallback sized rendition URL, not the original uploaded file URL. Alt text, optional rounded/responsive classes, and the existing size/orientation/crop mapping SHALL be preserved.

#### Scenario: WebP source and fallback img

- **WHEN** a page template calls `{% render_image %}` with a valid image and a mapped size
- **THEN** the output includes a `source` with `type="image/webp"` whose `srcset` is the WebP rendition URL
- **AND** the `img` `src` is the non-WebP sized rendition URL for the same dimensions

#### Scenario: Missing image is a no-op

- **WHEN** `{% render_image %}` is called with no image
- **THEN** the tag emits no markup and does not perform rendition lookups

### Requirement: Identical renditions are resolved once per request

Within a single request, the system MUST resolve each unique image and filter-spec pair at most once when serving `{% render_image %}`. Later calls with the same image and spec MUST reuse that rendition and MUST NOT issue another cache or database lookup for it.

#### Scenario: Same image repeated on one page

- **WHEN** `{% render_image %}` is invoked more than once in one request for the same image, orientation, size, prefix, and crop
- **THEN** only the first invocation performs the underlying rendition fetch for each of the WebP and fallback specs
- **AND** later invocations still emit the same URLs and classes

#### Scenario: Different specs stay independent

- **WHEN** the same image is rendered at two different sizes or crops in one request
- **THEN** each distinct filter spec is resolved separately

### Requirement: Tag contract stays compatible

Callers SHALL continue to use the existing `{% render_image %}` arguments (`image`, `orientation`, `size`, `size_prefix`, `alt_text`, `crop`, `rounded`, `responsive`). Changing those arguments MUST NOT be required for current block templates.

#### Scenario: Existing block templates keep working

- **WHEN** hero, cards, image-and-text, large-image, or small-image-and-text templates call `{% render_image %}` with their current arguments
- **THEN** they receive valid `<source>` and `<img>` markup without template changes
