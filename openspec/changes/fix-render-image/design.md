## Context

See proposal.md for motivation (Sentry RJF-6). `{% render_image %}` today builds a Django `Template` string, loads `wagtailimages_tags`, and runs two `{% image %}` tags per call. Each `{% image %}` calls Wagtail `get_rendition`, which Redis-`MGET`s `wagtail-rendition-<id>-<hash>-<filter>` and may `SELECT`/`SET` on a miss. The same image and spec can appear dozens of times on one `cms_page.html` render.

The fallback `<img>` interpolates `image.url` (original file) even though `{% image ... as the_image %}` already paid for a sized rendition. `_prefetch_block_images` on `CMSPageBase` is out of scope: it only loads image rows into an unused `_prefetched_images` dict and does not populate renditions.

Constraints: Wagtail 7 image API; no new runtime dependencies; keep the tag signature.

## Goals / Non-Goals

**Goals:**

- Resolve WebP and fallback renditions in Python and build the `<picture>` fragment from those URLs.
- Memoize renditions for `(image.pk, filter_spec)` on the current request.
- Point the `<img>` at the fallback rendition URL.

**Non-Goals:**

- Reworking StreamField image-id prefetch or attaching prefetched images onto block values (prior, separate issue).
- Changing `{% image %}` usage in carousel templates that do not go through `render_image`.
- Menu / `staff_only` navigation (UT-404).
- Adding a new public template tag or changing caller templates.

## Decisions

1. **Python `get_rendition` instead of an inner template**
   - Call `image.get_rendition(filter_spec)` (or Wagtail’s equivalent for the configured image model) for `"{spec}|format-webp"` and `"{spec}"`, then format HTML in the tag.
   - Alternative considered: keep `{% image %}` but cache the compiled template. That still does two rendition lookups per call and does not fix repeats.
   - Alternative considered: `prefetch_renditions` on the page queryset only. Useful later, but does not help unless the same image instances reach the tag; this change fixes the tag itself.

2. **Request-local memoization**
   - Store resolved renditions on `request` (or a ContextVar keyed for the request) keyed by `(image.pk, filter_spec)`.
   - First call may still hit Redis/DB; repeats in the same request must not.
   - Alternative considered: process-wide LRU. Rejected — renditions can change when images are recropped; request scope is enough for RJF-6.

3. **Keep two specs (WebP + fallback)**
   - Preserve the `<picture>` / `<source type="image/webp">` pattern. Do not drop the fallback rendition.

4. **Markup stays a fragment**
   - Callers wrap the tag in `<picture>`. The tag continues to emit `<source>` + `<img>` only, not an outer `<picture>`.

## Risks / Trade-offs

- **[Risk] Markup drift** if hand-built HTML misses a class or attribute → Mitigation: golden-string or HTML tests against current arguments (responsive, rounded, crop, alt).
- **[Risk] `get_rendition` API differences** on `CMSPageImage` vs `wagtailimages.Image` → Mitigation: use the instance’s own `get_rendition`; tests use `CMSPageImage`.
- **[Risk] Missing request** when the tag is rendered outside a request (tests, email) → Mitigation: memoize only when a request is present; otherwise call `get_rendition` directly.
- **[Trade-off] First lookup per spec still hits cache/DB.** Acceptable; the Sentry pattern is repeats of the same key.

## Migration Plan

- Deploy as a drop-in tag change; no migrations.
- Rollback is a revert of the tag module.
- Confirm in Sentry that RJF-6 `MGET` repeats for the same `wagtail-rendition-…` key drop after release (first-seen was a year ago; last-seen still current).

## Open Questions

- None that affect specs or the approach. Whether to later prefetch renditions onto StreamField images can be a follow-up.
