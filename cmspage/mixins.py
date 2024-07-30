import logging
import os
import json
from functools import cache, lru_cache
from itertools import combinations
from typing import List, Iterable, Dict, Optional

from django.conf import settings
from django.template import engines, TemplateDoesNotExist
from django.utils.functional import cached_property

CMSPAGE_TEMPLATE_STYLES = "CMSPAGE_TEMPLATE_STYLES"
CMSPAGE_TEMPLATE_BASE = "CMSPAGE_TEMPLATE_BASE"
CMSPAGE_TEMPLATE_BASE_DIR = "CMSPAGE_TEMPLATE_BASE_DIR"
CMSPAGE_TEMPLATE_INCLUDE_DIR = "CMSPAGE_TEMPLATE_INCLUDE_DIR"
CMSPAGE_TEMPLATE_INCLUDE_FILES = "CMSPAGE_TEMPLATE_INCLUDE_FILES"

DEFAULT_TEMPLATE_EXTENSIONS = [".html", ".htm"]
DEFAULT_BASE_TEMPLATE_NAME = "base.html"
DEFAULT_TEMPLATE_INCLUDE_NAMES = "title header navigation messages logo carousel main footer links contact media"

_logger = logging.getLogger("cmspage")


class CMSTemplateMixin:
    """
    Mixin to provide CMS template resolution logic.

    This mixin helps in determining the appropriate template to use
    for rendering CMS pages based on various conditions and settings.
    """
    """

    CMSTemplateMixin class provides a set of utility methods for handling templates and includes
    in CMS-related functionality.

    - `to_list(names: str | List[str] | None) -> List[str]`:
        - Converts a string of comma/space separated names to a list.
        - Parameters:
            - `names` (str | List[str] | None): The string or list of names to be converted.
        - Returns:
            - List[str]: The list of names.

    - `get_site_variables(request) -> dict`:
        - Returns the site variables for the current site.
        - Parameters:
            - `request`: The request object containing the current site information.
        - Returns:
            - dict: The site variables dictionary.

    - `base_template` (cached_property):
        - Returns the base template for the CMSTemplateMixin instance.
        - Returns:
            - str: The base template name.

    - `template_styles` (cached_property):
        - Returns the list of template styles available to support searching for templates.
        - Returns:
            - List[str]: The list of template styles.

    - `base_template_path` (cached_property):
        - Returns the base template path for the CMSTemplateMixin instance.
        - Returns:
            - str: The base template path.

    - `template_include_path` (cached_property):
        - Returns the path to template includes.
        - Returns:
            - str: The template include path.

    - `include_names` (cached_property):
        - Returns the list of include names for the CMSTemplateMixin instance.
        - Returns:
            - List[str]: The list of include names.

    - `get_include_templates()` (cache):
        - Returns a dictionary of include templates.
        - Returns:
            - Dict[str, str]: The dictionary of include templates.

    - `include_templates()`:
        - Returns a dictionary of include templates using the `find_existing_template()` method.
        - Returns:
            - dict: The dictionary of include templates.

    - `find_existing_template(template_path: str, *parts: Optional[str]) -> str | None` (lru_cache):
        - Returns an existing template path based on the additional path parts provided.
        - Parameters:
            - `template_path` (str): The base template path.
            - `*parts` (Optional[str]): Optional additional path parts.
        - Returns:
            - str | None: The existing template path if found, None otherwise.

    """

    default_base_template = DEFAULT_BASE_TEMPLATE_NAME
    default_template_dir = None
    default_include_dir = None
    template_extensions = DEFAULT_TEMPLATE_EXTENSIONS
    template_include_names = DEFAULT_TEMPLATE_INCLUDE_NAMES
    logging_level = logging.INFO

    @staticmethod
    def to_list(names: str | List[str] | None) -> List[str]:
        """
        Convert a string of comma/space separated names to a list,
        preserving the list if it is specified that way and returning
        an emptylist on blank string or None.

        """
        if isinstance(names, (str, bytes, bytearray)):
            return [name.strip() for name in names.replace(",", " ").split(" ")]
        elif isinstance(names, Iterable):
            return [name.strip() for name in names]
        return []

    @staticmethod
    def as_list(names: Iterable[str] | None) -> str:
        """
        Convert a list of names to a string

        """
        return ", ".join(names) if names else "None"

    @cached_property
    def template_debug(self) -> bool:
        """
        Return the template debug flag
        """
        return getattr(settings, "TEMPLATE_DEBUG", False)

    def log(self, message: str, *args, **kwargs) -> logging.Logger:
        if self.template_debug:
            level = logging.ERROR if kwargs.get("exc_info", False) else self.logging_level
            kwargs.setdefault("stacklevel", 2)
            _logger.log(level, message, *args, **kwargs)
        return _logger

    @cached_property
    def base_template(self) -> str:
        """
        Return the base template
        """
        base_template = getattr(settings, CMSPAGE_TEMPLATE_BASE, None) or self.default_base_template
        # Rule 1: if configured with a leading slash, remove it and use the rest as is
        if base_template.startswith("/"):
            base_template = base_template[1:]
        # Rule 2: if a base path is set, prepend it to the base template
        elif base_path := self.base_template_path:
            if not base_template.startswith(f"{base_path}/"):
                base_template = f"{base_path}/{base_template}"
        self.log(f"Base template: {base_template}")
        return base_template

    @cached_property
    def template_styles(self) -> List[str]:
        """
        Return the list of template styles available to support searching for templates.
        Styles assist in resolving where a template is sourced from and may represent
        css style, company styling or other variations.

        """
        styles = getattr(settings, CMSPAGE_TEMPLATE_STYLES, None)
        styles = self.to_list(styles)
        self.log(f"Template styles: {self.as_list(styles)}")
        return styles

    @cached_property
    def base_template_path(self) -> str:
        """
        Return the template path
        """
        base_path = getattr(settings, CMSPAGE_TEMPLATE_BASE_DIR, None) or self.default_template_dir
        self.log(f"Base template path: {base_path}")
        return base_path

    @cached_property
    def template_include_path(self) -> str:
        """
        Return the path to template includes
        """
        include_path = getattr(settings, CMSPAGE_TEMPLATE_INCLUDE_DIR, None) or self.default_include_dir
        include_path = f"{self.base_template_path}/{include_path}" if include_path else self.base_template_path
        self.log(f"Include path: {include_path}")
        return include_path

    @cached_property
    def include_names(self) -> List[str]:
        include_names = getattr(settings, CMSPAGE_TEMPLATE_INCLUDE_FILES, None) or self.template_include_names
        include_names = self.to_list(include_names)
        self.log(f"Include template names: {self.as_list(include_names)}")
        return include_names

    @cache
    def get_include_templates(self) -> Dict[str, str]:
        def append_template_extension(name):
            return name if any(name.endswith(ext) for ext in self.template_extensions) else f"{name}.html"

        def remove_template_extension(name):
            return name.rsplit(".")[0] if any(name.endswith(ext) for ext in self.template_extensions) else name

        includes = {
            remove_template_extension(include_name): append_template_extension(include_name)
            for include_name in self.include_names
        }

        include_templates = {
            include: f"{self.template_include_path}/{template_file}" for include, template_file in includes.items()
        }
        return include_templates

    @lru_cache(maxsize=128)
    def include_templates(self) -> dict:
        """
        Return a dictionary of include templates
        """
        templates = self.get_include_templates()
        resolved_include_paths = {
            include_name: template_name
            for include_name, include_path in templates.items()
            if (template_name := self.find_existing_template(include_path, *self.template_styles)) is not None
        }
        self.log(f"Resolved includes: {json.dumps(resolved_include_paths, indent=2)}")
        return resolved_include_paths

    @lru_cache
    def find_existing_template(self, template_path: str, *parts: Optional[str]) -> str | None:
        """
        Return an existing template path based on the additional path parts provided
        """
        dirname, filename = os.path.split(template_path)
        parts = [part for part in parts if part is not None]  # Filter possible None values

        # Generate all combinations of parts, from the longest to the shortest
        combinations_parts = sum(
            (
                ["/".join(subset) for subset in combinations(parts, r) if subset != ("",)]
                for r in range(len(parts), 0, -1)
            ),
            [],
        )
        # Generate all template paths and add the original template path as fallback
        templates = [f"{dirname}/{combination}/{filename}" for combination in combinations_parts] + [
            template_path
        ]

        for template_name in templates:
            for engine in engines.all():
                try:
                    _ = engine.engine.find_template(template_name)
                    self.log(f"Resolved template: {template_name}")
                    return template_name  # HIT
                except TemplateDoesNotExist:
                    pass
                except Exception:
                    self.log(f"Error resolving template: {template_name}", exc_info=True)
        # MISS, let the user figure this out
        return template_path
