# CMSPage

CMSPage is a package containing components and building blocks for a Wagtail CMS

## Quick start


1. Add `cmspage` to your `INSTALLED_APPS` setting like this:
```python
    INSTALLED_APPS = [
        ...
        'cmspage',
    ]
```
2. Run `python manage.py migrate` to create the `cmspage` models.
3. `CMSPage` should now be available as a page type in wagtail.
