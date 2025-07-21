# Wagtail CMSPage Module - Developer Documentation

## Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [StreamField Blocks](#streamfield-blocks)
6. [Models](#models)
7. [Template System](#template-system)
8. [Theme System](#theme-system)
9. [CSS Styling & Bootstrap Integration](#css-styling--bootstrap-integration)
10. [Navigation & Menus](#navigation--menus)
11. [Form System](#form-system)
12. [Template Tags](#template-tags)
13. [Context Processors](#context-processors)
14. [Extending CMSPageBase](#extending-cmspagebase)
15. [Performance & Optimization](#performance--optimization)
16. [Configuration Reference](#configuration-reference)
17. [Development Guidelines](#development-guidelines)

## Overview

The `wagtail-cmspage` module is a comprehensive content management system built on top of Wagtail CMS. It provides a rich set of StreamField blocks, models, and utilities for building flexible, themed websites with form capabilities, navigation management, and advanced template resolution.

### Key Features

- **Rich StreamField Blocks**: 20+ pre-built content blocks
- **Flexible Template System**: Multi-site, multi-framework template resolution
- **Theme System**: Semantic color palette with light/dark mode support
- **Navigation Management**: Hierarchical menu system with caching
- **Form Builder**: Dynamic form creation with validation
- **Performance Optimized**: Built-in caching and query optimization
- **Extensible Architecture**: Easy to extend and customize

## Core Concepts

### CMSPage Architecture

The module is built around several core concepts:

1. **CMSPageBase**: Abstract base class providing core functionality
2. **StreamField Blocks**: Reusable content components
3. **Template Mixin**: Advanced template resolution with fallbacks
4. **Theme System**: Semantic styling with CSS custom properties
5. **Navigation System**: Site-specific hierarchical menus

### Content Flow

```
User Content → StreamField Blocks → Template Resolution → Themed Output
```

## Installation

### Module Installation

Install using your preferred package manager:

```bash
# Using pip
pip install wagtail-cmspage

# Using uv
uv add wagtail-cmspage

# Using poetry
poetry add wagtail-cmspage
```

### Django Settings

Add to your Django project's `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.documents',
    'cmspage',
    # ... other apps
]

# Context processor for navigation
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                # ... other processors
                'cmspage.context_processors.cmspage_context',
            ],
        },
    },
]

# Optional: Enable WebP image conversion
WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'
```

### Run Migrations

```bash
python manage.py migrate cmspage
```

## Quick Start

### Basic Page Model

```python
# models.py
from cmspage.models import CMSPageBase
from wagtail.fields import StreamField

class MyCustomPage(CMSPageBase):
    # Use default body_blocks or extend them
    body = StreamField(CMSPageBase.body_blocks, blank=True)

    content_panels = CMSPageBase.content_panels
```

### Template Structure

```html
<!-- templates/myapp/my_custom_page.html -->
{% extends base_template %}
{% load cmspage_tags %}

{% block content %}
    {% include include.header %}

    {% for block in page.body %}
        {% include_block block %}
    {% endfor %}

    {% include include.footer %}
{% endblock %}
```

## StreamField Blocks

The module provides a comprehensive collection of StreamField blocks for different content types.

### Content Blocks

#### HeroImageBlock
**Purpose**: Large hero sections with background images

```python
# Usage in models.py
from cmspage.blocks import HeroImageBlock

body_blocks = [
    ('hero', HeroImageBlock()),
    # ... other blocks
]
```

**Fields**:
- `image`: Background image chooser
- `orientation`: landscape/portrait/square/extrawide
- `size`: tiny/small/medium/large/full_width/original
- `crop`: Crop percentage for positioning
- `rounded`: Border radius styling
- `responsive`: Enable responsive image sizes
- `palette`: Theme color from semantic palette
- `inset`: Padding/spacing options

**Template**: `blocks/hero_block.html`

#### CardsBlock
**Purpose**: Display sets of cards in responsive grid layout

```python
# Usage
body_blocks = [
    ('cards', CardsBlock()),
]
```

**Features**:
- Responsive grid (12/6/4/3 columns based on card count)
- Individual card styling options
- Automatic aspect ratio handling

**Card Fields**:
- `title`: Card heading
- `text`: Rich text content
- `image`: Optional card image
- `link`: Internal page or external URL
- `palette`: Individual card theming

#### CallToActionBlock
**Purpose**: Call-to-action sections with buttons

```python
body_blocks = [
    ('cta', CallToActionBlock()),
]
```

**Fields**:
- `title`: CTA heading (with cursive option)
- `text`: Rich text description
- `link`: Button link (page or URL)
- `justify`: Text alignment
- `palette`: Theme styling

#### ImageAndTextBlock
**Purpose**: Combined image and text content

**Variants**:
- `ImageAndTextBlock`: Standard image + text
- `SmallImageAndTextBlock`: Compact version
- `LargeImageBlock`: Image-focused variant

### Form Blocks

#### FormBlock
**Purpose**: Complete form builder with validation

```python
body_blocks = [
    ('form', FormBlock()),
]
```

**Features**:
- Dynamic field creation
- Client-side validation
- AJAX submission
- Success message handling
- Bootstrap styling

**Available Field Types**:
- `TextFieldBlock`: Single-line text input
- `TextAreaFieldBlock`: Multi-line text input
- `EmailFieldBlock`: Email validation
- `IntegerFieldBlock`: Numeric input with min/max
- `DecimalFieldBlock`: Decimal input with precision
- `SelectFieldBlock`: Dropdown with custom options
- `MultiSelectFieldBlock`: Multiple selection

### Utility Blocks

#### Navigation Blocks
- `LinksBlock`: Lists of internal/external links
- `SocialsBlock`: Social media link collections

#### Content Separators
- `NewSectionBlock`: Section dividers
- `LinesBlock`: Horizontal rules

#### Specialized Blocks
- `CarouselImageBlock`: Image carousels
- `CustomTableBlock`: Data tables
- `CopyrightBlock`: Copyright notices

### Complete Block Reference

```python
# All available blocks
from cmspage.blocks import (
    # Content blocks
    HeroImageBlock, CardsBlock, CallToActionBlock,
    ImageAndTextBlock, SmallImageAndTextBlock, LargeImageBlock,
    TitleBlock, RichTextWithTitleBlock,

    # Form blocks
    FormBlock, TextFieldBlock, TextAreaFieldBlock,
    EmailFieldBlock, IntegerFieldBlock, DecimalFieldBlock,
    SelectFieldBlock, MultiSelectFieldBlock,

    # Utility blocks
    NewSectionBlock, LinesBlock, CarouselImageBlock,
    CustomTableBlock, LinksBlock, SocialsBlock, CopyrightBlock,

    # Theme enums
    Palette, Heights, Insets, SocialIcon, IconColorChoices,
    Orientations, Justifications, ImageSizes, ImageAlignment
)
```

## Models

### Page Models

#### CMSPageBase (Abstract)
**Purpose**: Base class for all CMS pages

```python
from cmspage.models import CMSPageBase

class MyPage(CMSPageBase):
    # Inherit all CMSPageBase functionality
    pass
```

**Features**:
- Template resolution through CMSTemplateMixin
- SEO fields (keywords, descriptions)
- Tag management system
- Display options for titles and tags

**Default Fields**:
- `tags`: Page tagging system
- `display_title`: Toggle title display
- `display_tags`: Toggle tag display
- `seo_keywords`: SEO meta keywords

#### CMSPage (Concrete)
**Purpose**: Standard content pages

```python
# Built-in usage - no custom code needed
# Available in Wagtail admin as "CMS Page"
```

**Features**:
- Full StreamField with all blocks
- Hierarchical page structure
- Can be parent to other CMSPages

#### CMSHomePage
**Purpose**: Site homepage (limited to 1 per site)

**Special Features**:
- Hero block prioritized in admin
- Root-level page only
- Extended body_blocks with hero

#### CMSFooterPage
**Purpose**: Site footer content (limited to 1 per site)

**Features**:
- Specialized footer StreamField
- Contains: info, copyright, links, social blocks
- Integrated with context processor

#### CMSFormPage
**Purpose**: Form-enabled pages

**Features**:
- FormBlock + standard CMSPage blocks
- Form submission handling
- Success message display

### Supporting Models

#### MenuLink
**Purpose**: Navigation menu management

```python
# Access in templates via context processor
{{ navigation.main_menu }}
```

**Features**:
- Hierarchical menu structure
- Site-specific menus
- Staff-only menu items
- Automatic caching with invalidation
- Preview functionality

**Fields**:
- `site`: Site association
- `parent`: Hierarchical structure
- `menu_order`: Display order
- `menu_title`: Display text
- `link_page`: Internal page link
- `link_document`: Document link
- `link_url`: External URL
- `menu_icon`: FontAwesome icon
- `staff_only`: Staff visibility

#### CMSPageImage
**Purpose**: Enhanced image handling

**Features**:
- Automatic WebP conversion (optional)
- HEIF format support
- Extended metadata

## Template System

The template system provides advanced resolution with multi-site and multi-framework support through the `CMSTemplateMixin`.

### Template Resolution

The mixin resolves templates in this order:

1. Most specific path: `app/style1/style2/model.html`
2. Intermediate paths: `app/style1/model.html`, `app/style2/model.html`
3. Default path: `app/model.html`

### Configuration

```python
# settings.py
CMSPAGE_TEMPLATE_STYLES = ["mycompany", "bootstrap5"]
CMSPAGE_TEMPLATE_BASE = "cmspage/cmspage.html"
CMSPAGE_TEMPLATE_BASE_DIR = "cmspage"
CMSPAGE_TEMPLATE_INCLUDE_DIR = "includes"
CMSPAGE_TEMPLATE_INCLUDE_FILES = [
    "title", "header", "logo", "navigation", "navigation_item",
    "navigation_top", "navigation_item_top", "navigation_left",
    "navigation_item_left", "messages", "carousel", "main",
    "footer", "links", "contact", "media"
]
CMSPAGE_TEMPLATE_INCLUDE_FILES_EXTRA = ["custom_include"]
```

### Template Example

```html
<!-- myapp/mycompany/bootstrap5/my_custom_page.html -->
{% extends base_template %}
{% load cmspage_tags %}

{% block content %}
<div class="container">
    {% include include.header %}

    <main>
        {% if page.display_title %}
            <h1>{{ page.title }}</h1>
        {% endif %}

        {% for block in page.body %}
            {% include_block block %}
        {% endfor %}
    </main>

    {% include include.footer %}
</div>
{% endblock %}
```

### Include Template Usage

Include templates are automatically resolved and available in context:

```html
<!-- Navigation include -->
{% include include.navigation %}

<!-- Custom includes -->
{% include include.custom_include %}
```

### CMSTemplateMixin Methods

```python
from cmspage.mixins import CMSTemplateMixin

class MyView(CMSTemplateMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # base_template and include variables automatically available
        return context
```

## Theme System

The theme system provides semantic color classes with automatic light/dark mode support.

### Semantic Palette

```python
from cmspage.blocks.themes import Palette

# Available palette options
Palette.NONE          # cp-transparent - Transparent background
Palette.PAGE          # cp-page - Respects light/dark mode
Palette.LIGHT         # cp-light - Fixed light theme
Palette.DARK          # cp-dark - Fixed dark theme
Palette.WHITE         # cp-white - Black on white
Palette.BLACK         # cp-black - White on black
Palette.HIGHLIGHT     # cp-highlight - Highlight theme
Palette.STANDOUT      # cp-standout - Standout theme
Palette.SUCCESS       # cp-success - Success/positive
Palette.WARNING       # cp-warning - Warning/caution
Palette.INFO          # cp-info - Informational
Palette.DANGER        # cp-danger - Error/critical
```

### CSS Custom Properties

The theme system uses CSS custom properties that automatically adapt:

```css
/* Light mode (default) */
:root {
  --cp-fg-page: #548b8f;
  --cp-bg-page: #ffffff;
  --cp-fg-menu: #1a3d29;
  --cp-bg-menu: rgba(193, 215, 227, 0.1);
}

/* Dark mode */
[data-theme="dark"] {
  --cp-fg-page: #e0ffe0;
  --cp-bg-page: #1a1a1a;
  --cp-fg-menu: #b8e6b8;
  --cp-bg-menu: rgba(33, 47, 41, 0.1);
}

/* Auto mode (follows system preference) */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Dark mode variables */
  }
}
```

### Theme Utilities

```python
# Other theme options
from cmspage.blocks.themes import Heights, Insets

Heights.HEIGHT_0      # height-0
Heights.HEIGHT_1      # height-1
# ... through HEIGHT_5

Insets.INSET_0        # p-0
Insets.INSET_1        # p-1 p-sm-2 (responsive)
# ... through INSET_5
```

### Using Themes in Blocks

```python
from cmspage.blocks.themes import Palette, Insets
from wagtail import blocks

class MyCustomBlock(blocks.StructBlock):
    content = blocks.RichTextBlock()
    palette = blocks.ChoiceBlock(
        choices=Palette.choices,
        default=Palette.NONE
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices,
        default=Insets.INSET_3
    )

    class Meta:
        template = 'blocks/my_custom_block.html'
```

```html
<!-- blocks/my_custom_block.html -->
<div class="{{ block.palette }} {{ block.inset }}">
    {{ block.content }}
</div>
```

## CSS Styling & Bootstrap Integration

The wagtail-cmspage module provides a comprehensive CSS styling system built on Bootstrap 5 with an extensible semantic palette system. This allows for consistent theming across all components while maintaining full Bootstrap compatibility.

### SCSS Compilation

The module uses SCSS for styling and includes a compilation script for development. Whenever `cmspage.scss` or any of its included files are modified, the SCSS must be recompiled to CSS.

#### Requirements

- **sassc**: The Sass/SCSS compiler is required for compilation
- Install sassc using your system package manager:
  ```bash
  # macOS (Homebrew)
  brew install sassc

  # Ubuntu/Debian
  sudo apt-get install sassc

  # CentOS/RHEL
  sudo yum install sassc
  ```

#### Compilation Script

Use the provided compilation script to rebuild CSS files:

```bash
# Run from project root
./scripts/scss-compile.sh
```

**Script Features**:
- Automatically finds all `.scss` files (excluding partials starting with `_`)
- Builds include paths for imports
- Compiles to compressed CSS with source maps
- Outputs to `cmspage/static/css/`

**PyCharm Integration**:
The script can be configured as a File Watcher in PyCharm to automatically recompile SCSS files on save.

#### Including Compiled CSS

After compilation, include the generated CSS file in your templates. The `cmspage.css` file must be included **after** Bootstrap or Bootstrap enhancements to ensure proper styling:

```html
<!-- In your base template head section -->
...
<link rel="stylesheet" type="text/css" href="/static/css/styles.css">
<link rel="stylesheet" type="text/css" href="/static/css/cmspage.css">
...
```

**Important**: Always include `cmspage.css` after other stylesheets to ensure the semantic palette system and component variants override Bootstrap defaults correctly.

### Bootstrap 5 Foundation

The module is built on **Bootstrap 5** as its core styling foundation, providing:

- **Complete Bootstrap 5 compatibility**: All standard Bootstrap components work seamlessly
- **CSS Custom Properties integration**: Uses Bootstrap's modern CSS variable system
- **Responsive design**: Mobile-first approach with Bootstrap's grid system
- **Accessibility features**: ARIA support and screen reader compatibility
- **Modern browser support**: Uses CSS features like `color-mix()` and custom properties

### Palette-Based Component Variants

The module extends Bootstrap 5 with semantic palette variants for all major components:

#### Button Variants
```html
<!-- Standard Bootstrap -->
<button class="btn btn-primary">Primary Button</button>

<!-- Palette-based variants -->
<button class="btn btn-card">Card Theme Button</button>
<button class="btn btn-menu">Menu Theme Button</button>
<button class="btn btn-accent">Accent Theme Button</button>
<button class="btn btn-outline-card">Outlined Card Button</button>
```

#### Alert Variants
```html
<!-- Bootstrap alerts with palette theming -->
<div class="alert alert-card">Card themed alert</div>
<div class="alert alert-menu">Menu themed alert</div>
<div class="alert alert-accent">Accent themed alert</div>
```

#### Badge Variants
```html
<!-- Palette-based badges -->
<span class="badge badge-card">Card Badge</span>
<span class="badge badge-menu">Menu Badge</span>
<span class="badge badge-accent">Accent Badge</span>
```

#### Table Variants
```html
<!-- Palette-themed tables -->
<table class="table table-card">
<table class="table table-menu">
```

#### Card Variants
```html
<!-- Enhanced card theming -->
<div class="card card-menu">
<div class="card card-accent">
```

#### Form Control Variants
```html
<!-- Palette-styled form controls -->
<input type="text" class="form-control form-control-card">
<select class="form-select form-select-card">
```

### Default Color Scheme

The module provides sensible defaults based on Bootstrap 5's color system:

```css
/* Default color values (fallbacks) */
:root {
  --bs-primary: #0d6efd;      /* Bootstrap blue */
  --bs-secondary: #6c757d;    /* Bootstrap gray */
  --bs-success: #198754;      /* Bootstrap green */
  --bs-warning: #ffc107;      /* Bootstrap yellow */
  --bs-danger: #dc3545;       /* Bootstrap red */
  --bs-info: #0dcaf0;         /* Bootstrap cyan */
  --bs-light: #f8f9fa;        /* Bootstrap light */
  --bs-dark: #212529;         /* Bootstrap dark */
}
```

### Semantic Palette System

The palette system provides 12 semantic color themes that automatically adapt to light/dark modes:

```css
/* Semantic palette variables */
:root {
  --cp-fg-page: #548b8f;           /* Page text color */
  --cp-bg-page: #ffffff;           /* Page background */
  --cp-fg-menu: #1a3d29;           /* Menu text */
  --cp-bg-menu: rgba(193, 215, 227, 0.1);  /* Menu background */
  --cp-fg-accent: #39aa9b;         /* Accent color */
  --cp-bg-accent: rgba(255, 255, 227, 0.5); /* Accent background */
}

/* Dark mode variants */
[data-theme="dark"] {
  --cp-fg-page: #e0ffe0;
  --cp-bg-page: #1a1a1a;
  --cp-fg-menu: #b8e6b8;
  --cp-bg-menu: rgba(33, 47, 41, 0.1);
}
```

### Available Utility Classes

#### Color Utilities
```html
<!-- Foreground colors -->
<div class="cp-fg-page">Page text color</div>
<div class="cp-fg-menu">Menu text color</div>
<div class="cp-fg-accent">Accent text color</div>

<!-- Background colors -->
<div class="cp-bg-page">Page background</div>
<div class="cp-bg-menu">Menu background</div>
<div class="cp-bg-card">Card background</div>

<!-- Combined utilities -->
<div class="cp-page">Page theme (fg + bg)</div>
<div class="cp-menu">Menu theme (fg + bg)</div>
<div class="cp-accent">Accent theme (fg + bg)</div>
```

#### Border Utilities
```html
<div class="cp-border-card">Card border color</div>
<div class="cp-border-menu">Menu border color</div>
<div class="cp-border-accent">Accent border color</div>
```

#### Link Utilities
```html
<a href="#" class="cp-link">Themed link</a>
<a href="#" class="cp-link-menu">Menu styled link</a>
```

#### Opacity Utilities
```html
<div class="cp-opacity-75">75% opacity</div>
<div class="cp-opacity-50">50% opacity</div>
<div class="cp-opacity-25">25% opacity</div>
```

### Multi-Mode Theme Support

The styling system supports multiple display modes:

#### Light Mode (Default)
```css
:root {
  /* Clean, bright interface with dark text on light backgrounds */
  --cp-fg-page: #548b8f;
  --cp-bg-page: #ffffff;
}
```

#### Dark Mode
```css
[data-theme="dark"] {
  /* Dark backgrounds with light text for reduced eye strain */
  --cp-fg-page: #e0ffe0;
  --cp-bg-page: #1a1a1a;
}
```

#### Auto Mode
```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    /* Automatically follows system preference */
    --cp-fg-page: #e0ffe0;
    --cp-bg-page: #1a1a1a;
  }
}
```

#### Print Mode
```css
@media print {
  :root {
    /* High contrast black and white for optimal printing */
    --cp-fg-page: #000000;
    --cp-bg-page: #ffffff;
  }
}
```

#### High Contrast Mode
```css
@media (prefers-contrast: high) {
  :root {
    /* Enhanced contrast for accessibility */
    --cp-fg-page: #2c5d5f; /* Darker text */
    --cp-bg-page: #ffffff; /* Pure white background */
  }
}
```

### Template Integration

Use palette classes directly in your templates:

```html
<!-- StreamField blocks automatically apply palette -->
{% for block in page.body %}
  <div class="{{ block.palette }} {{ block.inset }}">
    {% include_block block %}
  </div>
{% endfor %}

<!-- Manual palette application -->
<div class="card cp-accent p-4">
  <h2 class="cp-fg-accent">Accent Themed Card</h2>
  <p>This card uses the accent color palette.</p>
  <button class="btn btn-accent">Accent Button</button>
</div>

<!-- Responsive design with Bootstrap grid -->
<div class="container cp-page">
  <div class="row">
    <div class="col-md-6 cp-menu p-3">
      <h3>Menu Themed Column</h3>
    </div>
    <div class="col-md-6 cp-card p-3">
      <h3>Card Themed Column</h3>
    </div>
  </div>
</div>
```

### Customizing the Palette

Override CSS custom properties to customize the palette:

```css
/* Custom site colors */
:root {
  --cp-fg-accent: #your-accent-color;
  --cp-bg-accent: #your-accent-background;
  --cp-fg-menu: #your-menu-color;
  --cp-bg-menu: #your-menu-background;
}

/* Custom dark mode colors */
[data-theme="dark"] {
  --cp-fg-accent: #your-dark-accent;
  --cp-bg-accent: #your-dark-accent-bg;
}
```

### Icon System

The module includes a comprehensive icon system with organized SVG icons:

```html
<!-- Social media icons -->
<i class="icon-facebook"></i>
<i class="icon-twitter"></i>
<i class="icon-linkedin"></i>

<!-- UI icons -->
<i class="icon-menu"></i>
<i class="icon-search"></i>
<i class="icon-close"></i>
```

### Typography Enhancements

Custom typography features beyond Bootstrap defaults:

```css
/* Custom font families */
.hellohoney { font-family: hellohoney, cursive, sans-serif; }
.alexbrush { font-family: alexbrush, cursive, sans-serif; }

/* Enhanced heading styles */
.page-title {
  font-size: 2.0em;
  width: fit-content;
  font-kerning: normal;
  color: var(--cp-fg-heading, var(--heading-color, inherit));
}
```

### Spacing System

Extended spacing utilities for layout control:

```html
<!-- Height utilities -->
<div class="height-0">No height</div>
<div class="height-1">Small height</div>
<div class="height-5">Large height</div>

<!-- Responsive insets (padding) -->
<div class="p-1 p-sm-2">Responsive padding</div>
<div class="p-3 p-md-4">Larger responsive padding</div>
```

### Best Practices

#### Using Palette Classes
```html
<!-- ✅ Good: Use semantic palette classes -->
<div class="cp-accent">Themed content</div>
<button class="btn btn-accent">Themed button</button>

<!-- ❌ Avoid: Hard-coded Bootstrap colors -->
<div class="bg-primary text-white">Hard-coded content</div>
```

#### Responsive Design
```html
<!-- ✅ Good: Combine with Bootstrap responsive utilities -->
<div class="cp-menu p-2 p-md-4 mb-3 mb-lg-5">
  Responsive themed content
</div>
```

#### Accessibility
```html
<!-- ✅ Good: Maintain semantic HTML with ARIA -->
<button class="btn btn-accent" aria-label="Submit form">
  <i class="icon-check" aria-hidden="true"></i>
  Submit
</button>
```

The CSS styling system provides a robust foundation for building modern, accessible, and themeable websites while maintaining full Bootstrap 5 compatibility and extending it with a powerful semantic palette system.

## Navigation & Menus

The navigation system provides hierarchical menus with caching and permission handling.

### MenuLink Model

```python
# Creating menu links programmatically
from cmspage.models import MenuLink

menu_link = MenuLink.objects.create(
    site=current_site,
    menu_title="About Us",
    link_page=about_page,
    menu_order=10,
    staff_only=False
)

# Creating submenus
submenu = MenuLink.objects.create(
    site=current_site,
    parent=menu_link,
    menu_title="Our Team",
    link_page=team_page,
    menu_order=10
)
```

### Template Usage

```html
<!-- Navigation provided by context processor -->
{% for item in navigation %}
    <a href="{{ item.url }}"
       class="nav-link {% if item.active %}active{% endif %}">
        {% if item.icon %}<i class="{{ item.icon }}"></i>{% endif %}
        {{ item.title }}
    </a>

    {% if item.children %}
        <ul class="submenu">
            {% for child in item.children %}
                <li><a href="{{ child.url }}">{{ child.title }}</a></li>
            {% endfor %}
        </ul>
    {% endif %}
{% endfor %}
```

### Performance Features

- **Automatic Caching**: Menu queries are cached and invalidated on changes
- **N+1 Prevention**: Optimized querysets prevent redundant database hits
- **Permission Filtering**: Staff-only items filtered based on user permissions

### Advanced Usage

```python
# Custom menu retrieval
from cmspage.models import MenuLink

# Get menu for specific site
menu_items = MenuLink.get_menu_links(site=request.site)

# Get hierarchical menu structure
menu_tree = MenuLink.get_menu_tree(site=request.site)
```

## Form System

The form system enables dynamic form creation with client-side validation and AJAX submission.

### FormBlock Structure

```python
# Form block in StreamField
body_blocks = [
    ('contact_form', FormBlock()),
]
```

### Form Configuration

FormBlock provides these fields:

- `form_title`: Form heading
- `form_description`: Instructional text
- `submit_url`: Form submission endpoint
- `submit_button_text`: Button label
- `success_message`: Post-submission message
- `fields`: Dynamic field collection

### Available Field Types

#### TextFieldBlock
```python
{
    'field_type': 'text',
    'label': 'Full Name',
    'help_text': 'Enter your full name',
    'required': True,
    'max_length': 100
}
```

#### EmailFieldBlock
```python
{
    'field_type': 'email',
    'label': 'Email Address',
    'required': True
}
```

#### SelectFieldBlock
```python
{
    'field_type': 'select',
    'label': 'Department',
    'options': [
        {'value': 'sales', 'label': 'Sales'},
        {'value': 'support', 'label': 'Support'}
    ],
    'required': True
}
```

### Form Submission Handling

The form system includes Bootstrap-styled templates and JavaScript for AJAX submission:

```javascript
// Built-in JavaScript handles:
// - Client-side validation
// - AJAX form submission
// - Success/error message display
// - Form reset after successful submission
```

### Custom Form Processing

```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process_form(request):
    if request.method == 'POST':
        # Process form data
        form_data = request.POST

        # Your custom processing logic

        return JsonResponse({
            'success': True,
            'message': 'Form submitted successfully!'
        })
```

## Template Tags

### render_image Tag

Advanced image rendering with responsive support:

```html
{% load cmspage_tags %}

<!-- Basic usage -->
{% render_image page.image %}

<!-- With parameters -->
{% render_image page.image orientation="landscape" size="medium" %}

<!-- Responsive images -->
{% render_image page.image responsive=True rounded=True %}

<!-- Custom alt text -->
{% render_image page.image alt_text="Custom description" %}
```

**Parameters**:
- `orientation`: landscape/portrait/square/extrawide
- `size`: tiny/small/medium/large/full_width/original
- `size_prefix`: Custom size prefix
- `alt_text`: Custom alt text
- `crop`: Crop percentage
- `rounded`: Bootstrap rounded classes
- `responsive`: Enable responsive images

**Size Matrix**:
```python
SIZES = {
    "tiny": ((150, 100), (100, 150), (150, 150), (450, 150)),
    "small": ((300, 200), (200, 300), (300, 300), (900, 300)),
    "medium": ((480, 320), (320, 480), (480, 480), (1440, 480)),
    "large": ((600, 400), (400, 600), (600, 600), (1800, 600)),
    "full_width": ((800, 533), (533, 800), (800, 800), (2400, 800)),
    "original": (None, None)  # No resizing
}
```

### embedurl Filter

Convert YouTube URLs to embeddable format:

```html
{% load cmspage_tags %}

<!-- Convert YouTube URL -->
{{ video_url|embedurl }}

<!-- Example -->
{{ "https://www.youtube.com/watch?v=dQw4w9WgXcQ"|embedurl }}
<!-- Outputs: https://www.youtube.com/embed/dQw4w9WgXcQ -->
```

## Context Processors

### cmspage_context

Combines navigation and site variables:

```python
# settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'cmspage.context_processors.cmspage_context',
            ],
        },
    },
]
```

**Provides**:
- `navigation`: Hierarchical menu structure
- `site`: Current site object
- `site_name`: Site name
- `site_hostname`: Site hostname
- `site_is_default`: Default site flag

### Individual Processors

```python
# Use individual processors if needed
'cmspage.context_processors.navigation',
'cmspage.context_processors.site_variables',
```

## Extending CMSPageBase

### Basic Extension

```python
from cmspage.models import CMSPageBase
from wagtail.fields import StreamField
from wagtail import blocks

class ProductPage(CMSPageBase):
    # Add custom fields
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Extend body_blocks
    custom_blocks = [
        ('price_display', blocks.StructBlock([
            ('price', blocks.DecimalBlock()),
            ('currency', blocks.CharBlock(default='USD')),
        ])),
    ]

    body_blocks = custom_blocks + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True)

    # Extend content panels
    content_panels = CMSPageBase.content_panels + [
        FieldPanel('price'),
    ]
```

### Advanced Extension

```python
from cmspage.blocks import CallToActionBlock, CardsBlock
from cmspage.blocks.themes import Palette, Insets

class EventPage(CMSPageBase):
    # Custom fields
    event_date = models.DateTimeField()
    registration_url = models.URLField(blank=True)

    # Custom blocks with theme support
    event_blocks = [
        ('event_hero', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('date', blocks.DateTimeBlock()),
            ('location', blocks.CharBlock()),
            ('palette', blocks.ChoiceBlock(choices=Palette.choices)),
        ], template='blocks/event_hero_block.html')),

        ('registration_cta', CallToActionBlock()),
        ('speaker_cards', CardsBlock()),
    ]

    # Combine with parent blocks
    body_blocks = event_blocks + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True)

    content_panels = CMSPageBase.content_panels + [
        FieldPanel('event_date'),
        FieldPanel('registration_url'),
    ]

    class Meta:
        verbose_name = "Event Page"
```

### Creating Custom Blocks

```python
from wagtail import blocks
from cmspage.blocks.themes import Palette, Insets

class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock()
    author = blocks.CharBlock()
    author_title = blocks.CharBlock(required=False)
    author_image = ImageChooserBlock(required=False)
    palette = blocks.ChoiceBlock(
        choices=Palette.choices,
        default=Palette.LIGHT
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices,
        default=Insets.INSET_3
    )

    class Meta:
        template = 'blocks/testimonial_block.html'
        icon = 'quote-left'
        label = 'Testimonial'
```

```html
<!-- blocks/testimonial_block.html -->
<blockquote class="testimonial {{ block.palette }} {{ block.inset }}">
    <p>"{{ block.quote }}"</p>
    <footer>
        {% if block.author_image %}
            {% render_image block.author_image size="tiny" orientation="square" %}
        {% endif %}
        <cite>
            {{ block.author }}
            {% if block.author_title %}<br><small>{{ block.author_title }}</small>{% endif %}
        </cite>
    </footer>
</blockquote>
```

## Performance & Optimization

### Caching Strategy

#### MenuLink Caching
```python
# Automatic caching with invalidation
from cmspage.models import MenuLink

# Cached query
menu_items = MenuLink.get_menu_links(site=request.site)

# Cache is automatically invalidated when MenuLinks change
```

#### Template Resolution Caching
```python
# LRU cache for template path resolution
from functools import lru_cache

@lru_cache(maxsize=128)
def find_existing_template(template_name, styles):
    # Cached template resolution
    pass
```

### Database Optimization

#### Optimized Querysets
```python
# MenuLink queries are optimized to prevent N+1
MenuLink.objects.filter(site=site).select_related(
    'link_page', 'link_document', 'parent'
).order_by('menu_order', 'id')
```

#### Bulk Operations
```python
# Support for bulk_create operations
MenuLink.objects.bulk_create([
    MenuLink(site=site, menu_title="Item 1"),
    MenuLink(site=site, menu_title="Item 2"),
])
```

### Image Optimization

#### WebP Conversion
```python
# settings.py
WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'

# Automatic WebP conversion on upload
class CMSPageImage(AbstractImage):
    def save(self, *args, **kwargs):
        # Convert to WebP if conditions are met
        super().save(*args, **kwargs)
```

#### Responsive Images
```html
<!-- Automatic responsive image generation -->
{% render_image image responsive=True %}
```

### Performance Monitoring

```python
# Monitor query performance
from django.db import connection

def get_menu_with_monitoring():
    initial_queries = len(connection.queries)
    menu_items = MenuLink.get_menu_links(site=site)
    final_queries = len(connection.queries)
    print(f"Menu queries: {final_queries - initial_queries}")
```

## Configuration Reference

### Required Settings

```python
# Minimal configuration
INSTALLED_APPS = [
    'wagtail.images',
    'wagtail.embeds',
    'wagtail.documents',
    'cmspage',
]

TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'cmspage.context_processors.cmspage_context',
            ],
        },
    },
]
```

### Optional Settings

```python
# Template configuration
CMSPAGE_TEMPLATE_STYLES = "mycompany,bootstrap5"  # or ["mycompany", "bootstrap5"]
CMSPAGE_TEMPLATE_BASE = "cmspage/cmspage.html"
CMSPAGE_TEMPLATE_BASE_DIR = "cmspage"
CMSPAGE_TEMPLATE_INCLUDE_DIR = "includes"
CMSPAGE_TEMPLATE_INCLUDE_FILES = [
    "title", "header", "logo", "navigation", "navigation_item",
    "navigation_top", "navigation_item_top", "navigation_left",
    "navigation_item_left", "messages", "carousel", "main",
    "footer", "links", "contact", "media"
]
CMSPAGE_TEMPLATE_INCLUDE_FILES_EXTRA = ["custom_header", "sidebar"]

# Image configuration
WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'

# RichText features
DEFAULT_RICHTEXTBLOCK_FEATURES = [
    "h2", "h3", "h4", "h5", "h6",
    "bold", "italic", "ol", "ul", "hr",
    "link", "document-link", "image", "embed",
    "code", "blockquote", "superscript",
    "subscript", "strikethrough"
]
```

### CSS Framework Examples

#### Bootstrap 5 Setup
```python
CMSPAGE_TEMPLATE_STYLES = ["bootstrap5"]
```

#### Multi-site Setup
```python
CMSPAGE_TEMPLATE_STYLES = ["company1", "bootstrap5"]
# Template resolution order:
# 1. app/company1/bootstrap5/model.html
# 2. app/bootstrap5/model.html
# 3. app/company1/model.html
# 4. app/model.html
```

## Development Guidelines

### Best Practices

#### Model Design
```python
# ✅ Good: Extend CMSPageBase
class MyPage(CMSPageBase):
    body = StreamField(CMSPageBase.body_blocks, blank=True)

# ❌ Bad: Extend CMSPage (concrete class)
class MyPage(CMSPage):  # This won't work
    pass
```

#### Block Creation
```python
# ✅ Good: Use theme system
class MyBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(choices=Palette.choices)
    inset = blocks.ChoiceBlock(choices=Insets.choices)

# ✅ Good: Provide proper meta
class Meta:
    template = 'blocks/my_block.html'
    icon = 'placeholder'
    label = 'My Custom Block'
```

#### Template Structure
```html
<!-- ✅ Good: Use mixin variables -->
{% extends base_template %}
{% include include.header %}

<!-- ❌ Bad: Hard-coded paths -->
{% extends "base.html" %}
{% include "header.html" %}
```

### Testing

```python
# Test CMSPageBase extensions
from django.test import TestCase
from cmspage.models import CMSPageBase

class TestMyPage(TestCase):
    def test_page_creation(self):
        page = MyPage(title="Test Page")
        page.save()
        self.assertEqual(page.title, "Test Page")

    def test_template_resolution(self):
        page = MyPage(title="Test")
        template = page.get_template(request)
        self.assertIsNotNone(template)
```

### Debugging

```python
# Debug template resolution
from cmspage.mixins import CMSTemplateMixin

mixin = CMSTemplateMixin()
template_name = mixin.find_existing_template('myapp/mypage.html', ['bootstrap5'])
print(f"Resolved template: {template_name}")

# Debug menu queries
from django.db import connection
from cmspage.models import MenuLink

connection.queries.clear()
menu = MenuLink.get_menu_links(site=site)
print(f"Queries executed: {len(connection.queries)}")
```

### Migration Notes

When upgrading from older versions, run migrations to update palette values:

```bash
python manage.py migrate cmspage
```

The migration will automatically convert old Bootstrap-based palette values to the new semantic cp-* system.

---

This documentation provides comprehensive coverage of the wagtail-cmspage module's features and capabilities. For additional support or feature requests, please refer to the project's issue tracker.
