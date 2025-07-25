from collections import defaultdict
import logging
from typing import List

from django.http import HttpRequest
from django.contrib.auth import get_user_model
from wagtail.models import Site

from .models import MenuLink

__all__ = ("navigation", "cmspage_context", "site_variables")

User = get_user_model()
logger = logging.getLogger("cmspage.context_processors")


def _nav_pages_for_site(site: Site, user: User|None) -> List[dict]:
    user_id = user.pk if user else 0
    cached_menu_links = MenuLink.get_cached_menu_links(site, user_id)

    tree = []
    id_to_link = {}
    unlinked = defaultdict(list)

    for link in cached_menu_links:
        # noinspection PyUnresolvedReferences
        if link.staff_only and not (user and user.is_active and (user.is_staff or user.is_superuser)):
            continue
        node = {
            "id": link.id,
            "title": link.menu_title or link.menu_link_title,
            "type": link.menu_link_type,
            "icon": link.menu_link_icon,
            "icon_color": link.menu_icon_color,
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
    user = request.user if request.user.is_authenticated else None
    site: Site = Site.find_for_request(request)
    return {"navigation": _nav_pages_for_site(site, user)}


def site_variables(request: HttpRequest) -> dict:
    """
    Provide site-specific variables for templates
    """
    try:
        site: Site = Site.find_for_request(request)
        return {
            "site": site,
            "site_name": site.site_name,
            "site_hostname": site.hostname,
            "site_is_default": site.is_default_site,
        }
    except Site.DoesNotExist:
        # No site found for this request
        return {
            "site": None,
            "site_name": "",
            "site_hostname": "",
            "site_is_default": False,
        }


def cmspage_context(request: HttpRequest) -> dict:
    # combines all the above context processors into one
    context = {}
    context.update(navigation(request))
    context.update(site_variables(request))
    return context
