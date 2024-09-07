# CMSPAGE

## Overview

The `cmspage` app provides an opinionated extension to the Wagtail CMS,
featuring a body `StreamField` with a number of custom Wagtail `Blocks`, or components.
Blocks in this StreamField can be ordered by the page author as desired.

## Installation

### Module

This module is installed in similar fashion to any python module, using a package manager such as [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/), [poetry](https://python-poetry.org/docs/basic-usage/), [pipenv](https://pipenv-searchable.readthedocs.io/install.html#installing-packages-for-your-project), or `uv`, for example.

> ⚠️ As with any Django or Wagtail module - like any other python package - it is
> best installed into a local virtual environment (poetry and pipenv will both
> enforce this by default).

### Django settings

Add the `cmspage` app to your Django project's `INSTALLED_APPS` setting:

```python
...
INSTALLED_APPS = [
    ...,
    'cmspage',
    ...
]
```

The `cmspage` body component contains fields that use `wagtail.images`,
`wagtail.embeds` and `wagtail.documents`, so these modules are also required in INSTALLED_APPS.

## Usage & API

### Page creation

CMSPage is a `Page` model, and can be created in the Wagtail admin interface, or programmatically, as with any other Wagtail `Page` model.
It delivers a few additional enhancements to the standard Wagtail `Page` model:

- includes a `StreamField` with a large number of pre-defined custom `Blocks`.

  > CMSPage functionality can be extended using the same method that panels are overridden,
  > by inheriting the abstract `CMSPageBase` class, overriding the `body` field,
  > and adding additional blocks to those defined in the parent.
  >

  The provided `CMSHomePage` model is a simple example of this, which adds a hero block type to the
  base (abstract) CMSPageBase.

  A more extensive example which adds more additional blocks to the `CMSPageBase` is shown below:

```python
from cmspage.models import CMSPageBase
...
class MyCMSPage(CMSPageBase):
    body_blocks = [
        ('heading', blocks.CharBlock(icon='title', classname='title')),
        ('paragraph', blocks.RichTextBlock(icon='pilcrow', classname='paragraph')),
        ('image', ImageChooserBlock(icon='image', classname='image')),
        ('video', EmbedBlock(icon='media', classname='video')),
        ('button', ButtonBlock(icon='link', classname='button')),
    ] + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True)
    footnote = RichTextField(blank=True)
```

Note that the `body_blocks` list is prepended with the blocks defined in the parent class, `CMSPageBase`.
This is to ensure that the parent blocks are included in the child class,
so that child class can add additional blocks as required.
Additional blocks can be added before or after the parent blocks.

> Note that additional types of CMSPages you define need to use `CMSPageBase` as the parent class,
> not `CMSPage`.
> This is because Django doesn't allow fields to be overridden in child classes unless the
> parent class is abstract (and `CMSPageBase` is indeed abstract).

### Multi-site and CSS framework support

Using a configurable template path, the CMSPage app supports multiple site and alternative
CSS framework configurations by providing easily customisable template paths.

The default name for CMSPage templates, with no other customisation,
provides the same default template name that any other Django or Wagtail model uses.
This can also be manually overridden in the same way, using the `template_name`
class variable or overriding the `get_template` method.

However, CMSPage provides an alternative that allows templates to gracefully fall back to the default
through the CMSTemplateMixin class.
This mixin adds special handling through a number of Django settings that can vary this behaviour.

### CMS_TEMPLATE_STYLES

This setting is a list of none, one or more strings that represent CSS frameworks or sites.

The setting can be expressed as a python list of strings, a space- or comma-separated list of strings.
The default is an empty list, which adds no additional components to the default path used for cmspage template names.

- As per normal Django/Wagtail model template names, the default template is
  `<appname>/<snake-case-model>.html`.

  As an example, a model named `MyCMSPage` in an app named `mycmspages` would have the
  default template path of `mycmspages/my_cms_page.html`.

- If CMSPAGE_TEMPLATE_STYLES is in settings and set to `"bootstrap5"` or `["bootstrap5"]`,
  then the mixin first checks if `<appname>/bootstrap5/<snake-case-model>.html` exists,
  and if so, uses that by default.
  If it doesn't exist, then the template name falls back to the default.

- If CMSPAGE_TEMPLATE_STYLES is in settings and set to `"mycompany bootstrap5"` or `["mycompany", "bootstrap5"]`, then the mixin checks for the following until it finds a template that exists:

  - `<appname>/mycompany/bootstrap5/<snake-case-model>.html`
  - `<appname>/bootstrap5/<snake-case-model>.html`
  - `<appname>/mycompany/<snake-case-model>.html`
  - `<appname>/<snake-case-model>.html` (the default)

  Note that the longest path is checked first, so that the most specific matching template is always used.

There is only a small performance cost in the implementation of this scheme because the template name
and the existence of each template is only checked once, and the resolved full template name is cached.

Taking advantage of style configuration can be useful in supporting multiple sites
with fallbacks to a default template where a company-specific template doesn't exist.
Alternatively, it is possible to create versions of pages which can be used
with different front-end CSS frameworks—such as "bootstrap5" or "tailwindcss".

### CMSPAGE_TEMPLATE_BASE

This is the name of the base template that the CMSPage templates extend.
The default is `"base.html"` with the "cmspage" app name pre-pended,
which is a minimal template that includes the global base template.

While there is no compelling reason to change this setting, it is provided for maximum flexibility.

When using this setting, the base template is extended as follows:

```html
{% extends base_template %}
```

which, unless overridden, is effectively equivalent to using the string literal:

```html
{% extends "cmspage/cmsbase.html" %}
```

### CMSPAGE_TEMPLATE_BASE_DIR

By default, models deriving from `CMSPageBase` use the app name of the model.
This setting allows this to be overridden so that the entire hierarchy of templates used
is consistent, even across apps.


### CMSPAGE_TEMPLATE_INCLUDE_DIR

This setting provides the directory that contains included template files.

The default value is None, or blank, which means that the included templates are in the same directory as the main template.

### CMSPAGE_TEMPLATE_INCLUDE_FILES

This setting is a list of template files that are used in cmspage templates.

The default value is a list with the following contents:
```python
[
  "title",
  "header",
  "navigation",
  "navigation_item",
  "messages",
  "logo",
  "carousel",
  "main",
  "footer",
  "links",
  "contact",
  "media",
]
```
This setting may be either a list of strings or a space and/or comma-seprated string.

### CMSPAGE_TEMPLATE_INCLUDE_FILES_EXTRA

This setting is a list of additional include files that can used in cmspage templates.

It is an empty list by default.

This is typically used to augment the default set of include files without having to redefine it.

## Using include files

Include files are used in the CMSPage templates using the standard Django syntax, {% include ... %}.
Instead of using a string literal, the include tag uses a variable that is set in the context by the CMSTemplateMixin.
Do not specify the extension of the template file; this is added by default.
For example:

```
{% include include.header %}
{% include include.navigation %}
{% include include.main %}
{% include include.footer %}
```
