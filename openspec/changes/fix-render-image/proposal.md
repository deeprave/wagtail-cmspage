## Why

Sentry issue RJF-6 reports an N+1 while rendering `cmspage/cms_page.html`: dozens of Redis `MGET`s (and follow-up `SELECT`/`SET`) for the same Wagtail rendition of one image (`fill-533x800|format-webp`, image 8). The lookups come from `{% render_image %}`, which compiles a fresh Django template and runs two `{% image %}` tags on every call. This is not the earlier StreamField image-row prefetch problem; that path only loads `CMSPageImage` models and is unused by templates.

## What Changes

- Resolve WebP and fallback renditions in Python inside `render_image` instead of compiling and rendering an inner `{% image %}` template on every call.
- Reuse renditions for the same image and filter spec within a request so repeated tags (same image, same size) do not each hit Redis/DB.
- Emit a `<picture>` source/img pair that uses the WebP rendition URL and the fallback **rendition** URL (today the `<img>` uses `image.url`, the original file, after still paying for a second `{% image %}` lookup).
- Keep the public tag signature and visual output (size map, crop, rounded, responsive classes, alt text) unchanged.

## Capabilities

### New Capabilities

- `render-image`: CMS image tag that builds a WebP `<picture>` from cached/prefetched renditions without per-call template compilation or repeated identical rendition lookups.

### Modified Capabilities

- None. There is no existing `openspec/specs/` capability for this tag.

## Impact

- `cmspage/templatetags/cmspage_tags.py` (`render_image`)
- Templates that already call the tag (`hero`, `cards`, `image_and_text`, `large_image`, `small_image_and_text`)
- Wagtail `get_rendition` / rendition cache behaviour during `cms_page.html` render
- Tests around `render_image` and rendition reuse
- Does not change menu assembly or `staff_only` visibility (UT-404)
