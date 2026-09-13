## 1. Coverage

- [ ] 1.1 Add `tests/test_templatetags_render_image.py` that asserts `{% render_image %}` emits a WebP `source` and an `img` whose `src` is the fallback rendition URL (not the original file), and verify those assertions fail on current code
- [ ] 1.2 Add a request-scoped test that calls `render_image` twice with the same image and spec and asserts `get_rendition` runs once per spec, and verify the test fails on current code
- [ ] 1.3 Add a test that two different sizes for the same image each call `get_rendition` for their own specs, and verify it passes after implementation

## 2. Tag implementation

- [ ] 2.1 Replace the inner Django `Template` / `{% image %}` path in `render_image` with Python `get_rendition` for `"{spec}|format-webp"` and `"{spec}"`, and verify 1.1 passes
- [ ] 2.2 Memoize renditions on the current request keyed by `(image.pk, filter_spec)`, falling back to a direct `get_rendition` when no request is present, and verify 1.2 and 1.3 pass
- [ ] 2.3 Return empty output and skip rendition lookups when `image` is missing, and verify with a unit test

## 3. Compatibility

- [ ] 3.1 Keep the existing `render_image` arguments and `<source>` / `<img>` fragment (no wrapping `<picture>`), and verify `uv run pytest tests/test_templatetags.py tests/test_templatetags_render_image.py` passes
