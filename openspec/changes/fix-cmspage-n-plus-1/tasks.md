## 1. Coverage

- [ ] 1.1 Add `tests/test_models_cms_page_routing.py` that builds a live 3+ segment CMS tree under a home page, calls `route` / serve, and asserts child-by-slug lookups do not scale with depth; verify the assertion fails on current `Page.route`
- [ ] 1.2 Add tests that a live nested URL serves the leaf page, an unknown slug returns 404, and an unpublished leaf returns 404; verify they pass against current routing
- [ ] 1.3 Add a leftover-path test: full path is not a page, a shorter prefix page implements extra routing, and leftover components reach that page; verify it fails or is skipped until `route` is overridden
- [ ] 1.4 Add a view-restriction test that an unauthorized request does not receive the restricted page body; verify it passes against current routing

## 2. Route implementation

- [ ] 2.1 Override `route` on `AbstractCMSPage` to resolve remaining slugs via exact constructed `url_path` (longest prefix first, no `.live()` filter on the walk) and then `page.specific.route(request, leftover)`; verify 1.1 and 1.2 pass
- [ ] 2.2 Raise `Http404` when no prefix matches; verify the unknown-slug case in 1.2 still passes
- [ ] 2.3 Leave leftover components for the matched page’s `route`; verify 1.3 passes
- [ ] 2.4 Do not bypass Wagtail view restrictions; verify 1.4 still passes

## 3. Compatibility

- [ ] 3.1 Run `uv run pytest tests/test_models_cms_page_routing.py tests/test_cmspage.py` and confirm existing CMS page tests still pass
