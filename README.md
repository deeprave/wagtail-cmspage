# CMSPage

CMSPage is a package containing components and building blocks for a Wagtail CMS.
This class is designed to be flexible and usable in its own right. HGowever, as with any Wagtail page type, it can be extended and customised to suit your needs.

At the core, CMSPage is a Wagtail page with a StreamField with orderable blocks of various types. It supports many features of of the box including bootstrap styled templates (which can be easily changed), and supports multiple sites by allowing for site-specific variables.

## Quick start / Installation

1. Once added to your virtual environmebnt, add `cmspage` to INSTALLED_APPS in your Django settings:
```python
    INSTALLED_APPS = [
        ...
        'cmspage',
    ]
```
2. Run `python manage.py migrate` to create the `cmspage` models.
3. `CMSPage` should now be available as a page type in wagtail.

## Configuration
