## Context

See proposal.md (Why). Wagtail’s default `Page.route` does `get_children().get(slug=segment)` then `subpage.specific.route(...)` for each remaining component. That matches Sentry RJF-36: repeated `wagtailcore_page` filters on `depth` / `path BETWEEN` / `slug`, then `cmspage_cmspage` JOIN on `page_ptr_id`. CMS page types inherit `Page.route` unchanged. Site serve still starts at the site root’s `specific.route`; we only change how a CMS page consumes the remaining path.

## Goals / Non-Goals

**Goals:**

- Override routing on the shared CMS page base so every CMS type (home, page, form, footer) resolves the remaining path without a per-segment child + `specific` pair.
- Keep live/404 and view-restriction behaviour aligned with Wagtail’s default router.
- Support leftover path components via longest matching `url_path` prefix.

**Non-Goals:**

- Changing `{% render_image %}` (RJF-6 / `fix-render-image`).
- MenuLink / navigation assembly.
- StreamField image prefetch or `CMSFooterPage.objects.live().first()` in `get_context`.
- Removing Wagtail multi-table `specific()` entirely (one subclass fetch for the matched page is expected).

## Decisions

1. **Override `route` on `AbstractCMSPage`**
   - **Why**: All concrete CMS types inherit it; `Site` already calls `root.specific.route`. One implementation covers the Sentry `cmspage_cmspage` JOIN pattern.
   - **Alternative**: Custom `serve` view or middleware path cache — wider surface, easier to miss Wagtail’s live/restriction checks.

2. **Resolve by constructed `url_path`, longest prefix first**
   - Build candidates from `self.url_path` plus remaining slugs (Wagtail `url_path` is slash-terminated). Try the full path, then shorter prefixes, until a `Page` row exists (do **not** filter `.live()` on the walk — default `get_children()` includes non-live nodes; only the leaf `route([], …)` applies the live check).
   - Call `page.specific.route(request, leftover_components)` so the matched page (CMS or not) keeps its own serve/routable behaviour.
   - **Alternative**: Prefetch the whole descendant tree from the root — unbounded and worse for large sites.
   - **Alternative**: Redis-cache resolved paths — stale URLs after moves/unpublish unless we add invalidation.

3. **No match → `Http404` (same as default)**
   - If no prefix matches, raise `Http404` rather than walking slugs again. Default routing would also 404.

4. **Tests assert query shape, not just status codes**
   - Capture queries during `page.route` / client get for a 3+ segment live tree. Fail if child-by-slug lookups scale with depth. Compatibility cases: 404, unpublished leaf, leftover path on a page that implements extra routing.

## Risks / Trade-offs

- **[Risk] Skipping intermediate `route()` overrides** → Default Wagtail only uses intermediate `route` to walk. A site-specific page type with a custom `route` in the middle of a CMS tree would not run if we jump to a deeper `url_path`. Mitigation: project `subpage_types` are CMS pages plus stock `Page`; stock `Page.route` has no extra serve logic. Document the assumption.
- **[Risk] `url_path` prefix collisions** → Use exact constructed paths (`…/foo/` vs `…/foobar/`), never `startswith` without a trailing slash boundary.
- **[Risk] Locales / aliases** → Base candidates on the current page’s `url_path` so locale prefixes stay. Aliases keep their own `url_path`; `specific()` remains Wagtail’s.
- **[Trade-off] A few prefix queries on routable leftover paths** → Still bounded by leftover length, not by successful page depth; typical CMS URLs match on the first (full-path) try.

## Migration Plan

- Deploy the package version; no schema or data migration.
- Rollback: revert the `route` override; URLs were unchanged.

## Open Questions

None. Footer `get_context` lookup and rendition N+1 stay on their own tracks.
