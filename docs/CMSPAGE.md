# CMSPAGE
## Overview

The `cmspage` app provides an opinionated extension to the Wagtail CMS, featuring a `StreamField` with a number of custom Wagtail `Blocks`, or components.
Blocks in this StreamField can be ordered, and re-ordered by the page author as desired.

## Installation
### Module
This module is installed in similar fashion to any python module, using a package manager such as [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/), [poetry](https://python-poetry.org/docs/basic-usage/), [pipenv](https://pipenv-searchable.readthedocs.io/install.html#installing-packages-for-your-project), or `uv`, for example.
> ⚠️ As with any Django, Wagtail and almost any other python - module,  it is best installed into a local virtual environment (poetry and pipenv will both enforce this by default).

### Django settings
Add the `cmspage` app to your Django project's `INSTALLED_APPS` setting:
```python
INSTALLED_APPS = [
    ...,
    'cmspage',
    ...
]
```
`cmspage` uses `wagtail.images`, `wagtail.embeds` and `wagtail.documents` which are also required in INSTALLED_APPS.

## Usage & API



### Page creation

CMSPage is a `Page` model, and can be created in the Wagtail admin interface, or programmatically, as with any other Wagtail `Page` model.
It delivers a few additional enhancements to the standard Wagtail `Page` model:
- includes a `StreamField` with a number of pre-defined custom `Blocks`. This can be easily extended using the same method that panels are overridden, by inheriting the CMSPage class, adding a `body` to override the parent field, and adding additional blocks to those defined in the parent. The `CMSHomePage` is a good example of this, which adds a hero block type to the home page.
```python

```
