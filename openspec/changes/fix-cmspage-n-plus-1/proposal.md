## Why

Sentry issue RJF-36 is an N+1 on page serve (`http.server` / `/{var}`): Wagtail walks each URL slug with `get_children().get(slug=…)` and then `.specific`, so a nested CMS page repeats `wagtailcore_page` path/slug lookups and `cmspage_cmspage` JOIN fetches. `AbstractCMSPage` does not override `route()`, so every hop pays both queries. This is not MenuLink assembly and not the `render_image` rendition N+1 (RJF-6).

## What Changes

- Resolve a request path to the target CMS page without one child-lookup-plus-`specific()` pair per URL segment.
- Keep published URLs, 404s, draft/live rules, and view restrictions the same as Wagtail’s default router.
- Still support leftover path components for routable descendants (longest matching page prefix, then `specific.route` with the remainder).
- Leave MenuLink, `{% render_image %}`, and StreamField image prefetch to their own changes.

## Capabilities

### New Capabilities

- `cms-page-routing`: Serve-time resolution of CMS page URLs in a bounded number of page/`specific` queries, independent of path depth.

### Modified Capabilities

- None. There is no existing `openspec/specs/` capability for page routing.

## Impact

- `cmspage/models/cms_page.py` (`AbstractCMSPage` / shared page types: `CMSHomePage`, `CMSPage`, `CMSFormPage`, `CMSFooterPage`)
- Wagtail `Page.route` behaviour for trees whose ancestors are CMS page types
- Tests for serve/route query counts and URL compatibility
- Does not change menu assembly, `staff_only`, or rendition tags
