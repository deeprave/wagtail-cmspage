from collections import defaultdict
import logging
from functools import cache
from typing import List

from django.conf import settings
from django.http import HttpRequest
from wagtail.models import Site

from .models import SiteVariables, MenuLink

__all__ = ("navigation", "site_variables", "cmspage_context")

logger = logging.getLogger("cmspage.context_processors")


def _nav_icon_path(icon: str) -> str:

    @cache
    def _nav_icon_base():
        return getattr(settings, "CMSPAGE_NAV_ICON_PATH", "images/icons")

    return f"{_nav_icon_base()}/{icon}.svg" if icon else ""


def _nav_pages_for_site(site: Site, user_id: int) -> List[dict]:
    cached_menu_links = MenuLink.get_cached_menu_links(site, user_id)

    tree = []
    id_to_link = {}
    unlinked = defaultdict(list)

    for link in cached_menu_links:
        node = {
            "id": link.id,
            "title": link.menu_title or link.menu_link_title,
            "type": link.menu_link_type,
            "icon": _nav_icon_path(link.menu_link_icon),
            "url": link.url,
            "children": [],
        }
        id_to_link[link.id] = node

        if link.parent:
            if parent := id_to_link.get(link.parent.id):
                parent["children"].append(node)
                continue
            # Handle orphaned nodes or log an error
            unlinked[link.parent].append(node)
        else:
            tree.append(node)

    if unlinked:
        for parent_id, children in unlinked.items():
            if parent := id_to_link.get(parent_id):
                parent["children"].extend(children)
            else:
                logger.error(f"Orphaned menu link(s): {children}")
    return tree


def navigation(request: HttpRequest) -> dict:
    user_id = request.user.id if request.user.is_authenticated else 0
    site: Site = Site.find_for_request(request)
    return {"navigation": _nav_pages_for_site(site, user_id)}


def site_variables(request: HttpRequest) -> dict:
    site: Site = Site.find_for_request(request)
    site_vars = SiteVariables.get_cached_variables(site)
    return {"site": site_vars}


def cmspage_context(request: HttpRequest) -> dict:
    # combines all the above context processors into one
    return navigation(request) | site_variables(request)
