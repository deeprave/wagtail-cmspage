# CMSPage

CMSPage is a package containing ready-to-use components and building blocks for a Wagtail CMS.
This class is designed to be flexible and usable in its own right without needing to build site-specific extensions.
However - as with any Wagtail page type - it can be extended and customised to suit your needs.

CMSPage is fundamentally a Wagtail page featuring a StreamField with various orderable blocks.
It offers numerous built-in features, such as easily customisable Bootstrap-styled templates and
support for multiple sites with site-specific variables.
CMSPage aims to address a wide range of needs, reducing the time required to build a new CMS site
and minimizing the need for additional extensive model and template design.

<a name="installation"></a>
## Quick start / Installation

1. Once added to your virtual environment, add `cmspage` to INSTALLED_APPS in your Django settings:

```python
INSTALLED_APPS = [
    ...
    'cmspage',
    ...
]
```

2. Run `python manage.py migrate` to create the `cmspage` models.
3. `CMSPage` should now be available as a page type in wagtail.

<a name="configuration"></a>
## Configuration

This package offers numerous settings to adjust its behaviour to your needs.
The default settings are designed to work out of the box, so customisation is optional.

Almost all of these settings can be found in the [developer reference](docs/CMSPAGE.md#django-settings).

<a name="templates"></a>
## Templates

Take note of how the CMSPage template system works, even if you don't plan to customise it.
The linking of templates and blocks are the core of the cmspage package, and understanding how they work will help you
in designing your pages and deciding on if and how to extend them.

This package is fully extensible and built on Wagtail's own extensibility.
You can add your own blocks, or even override the entire CMSPage model with your own custom classes if you wish, add
additional blocks to the core `body` StreamField, add fields and modify templates more to your liking.

The key benefit of CMSPage is that it provides a large number of blocks out of the box, and a number of templates that
are ready to use, so you can get started quickly and easily without having to develop custom templates for your page
models.
