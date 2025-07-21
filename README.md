# wagtail-cmspage

**A comprehensive content management solution for Wagtail CMS**

wagtail-cmspage provides ready-to-use page types, content blocks, and templates that accelerate CMS development. Built on Wagtail's StreamField architecture, it offers a complete content editing experience with Bootstrap 5 styling, theme switching, and flexible template systems.

## 🚀 Features

### 📝 **Rich Content Blocks**
- **Hero Images** - Eye-catching banners with overlay text
- **Cards** - Flexible card layouts for content organization
- **Image & Text** - Side-by-side content with responsive layouts
- **Rich Text** - Full WYSIWYG editing with custom styling
- **Call-to-Action** - Prominent buttons and conversion elements
- **Tables** - Custom styled data tables
- **Carousels** - Image slideshows and galleries
- **Forms** - Dynamic form creation with field validation

### 🎨 **Bootstrap 5 Integration**
- Semantic color palette system with CSS custom properties
- Light/dark theme switching with system preference detection
- Responsive utilities and component variants
- Custom Bootstrap overrides for CMS-specific styling

### 🔧 **Developer Features**
- Advanced template resolution system supporting multiple CSS frameworks
- Hierarchical include template system with safe fallbacks
- Configurable template styles and paths
- Built-in caching and performance optimizations
- Extensible mixins for custom page types

### 👥 **Content Editor Experience**
- Intuitive drag-and-drop page building
- Live preview of content changes
- SEO-friendly meta fields and tagging
- Consistent styling across all content blocks

## 📦 Installation

### Requirements
- Python 3.8+
- Django 4.2+
- Wagtail 5.0+

### Quick Start

1. **Install the package:**
   ```bash
   pip install wagtail-cmspage
   # or with uv
   uv add wagtail-cmspage
   ```

2. **Add to Django settings:**
   ```python
   INSTALLED_APPS = [
       ...
       'cmspage',
       ...
   ]
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create your first CMS page:**
   - Go to Wagtail Admin → Pages → Add child page
   - Select "CMS Page" from the page types
   - Start building with drag-and-drop content blocks

## 🎯 Quick Example

```python
# Basic usage - no additional code needed!
# CMSPage works out of the box with default templates and styling

# For custom implementations:
from cmspage.models import CMSPageBase

class CustomPage(CMSPageBase):
    # Add your custom fields
    custom_field = models.CharField(max_length=255, blank=True)

    # Customize available blocks
    body_blocks = CMSPageBase.body_blocks + [
        ('custom_block', MyCustomBlock()),
    ]
```

## 📚 Documentation

- **[Developer Reference](docs/CMSPAGE.md)** - Complete technical documentation
- **[Content Editor Guide](docs/CONTENT_EDITOR_GUIDE.md)** - User manual for content creators
- **[ChangeLog](ChangeLog.md)** - Version history and release notes

## 🔗 Template System

wagtail-cmspage uses an advanced template resolution system that supports:

- **Multiple CSS frameworks** (Bootstrap, Tailwind, etc.)
- **Hierarchical template discovery** with style-based overrides
- **Include template system** with safe fallbacks using `{% cmspage_include %}`
- **Theme switching** with CSS custom properties

```django
<!-- Template usage example -->
{% load cmspage_tags %}

<!-- Safe includes that handle missing templates gracefully -->
{% cmspage_include include.header %}
{% cmspage_include include.navigation %}
{% cmspage_include include.theme_switcher %}
```

## 🎨 Theming

Built-in support for light/dark themes with automatic system preference detection:

```html
<!-- Theme switcher automatically included -->
<div class="theme-switcher-fixed">
  <!-- Light/Auto/Dark mode buttons -->
</div>
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for details on how to:

- Report bugs and request features
- Submit pull requests
- Improve documentation
- Add new content blocks

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the Wagtail community**
