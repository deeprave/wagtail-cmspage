from typing import List

from django.http import HttpRequest
from wagtail.models import Site

from .models import SiteVariables, MenuLink

__all__ = ("navigation", "site_variables", "cmspage_context")


def _nav_pages_for_site(site: Site, user_id: int) -> List[dict]:
    cached_menu_links = MenuLink.get_cached_menu_links(site, user_id)

    links = [
        {
            "id": link.id,
            "parent_id": link.parent.id if link.parent else None,
            "title": link.menu_title or link.menu_link_title,
            "type": link.menu_link_type,
            "icon": link.menu_link_icon,
            "url": link.url,
            "children": [],
        }
        for link in cached_menu_links
    ]

    # build a map of links by id
    id_to_link = {link["id"]: link for link in links}

    # use a list comprension to add parent nodes to the tree
    tree = [id_to_link[link["id"]] for link in links if not link["parent_id"]]

    # If each link has a parent, add it to the parent's children
    for link in links:
        parent_id = link["parent_id"]
        if parent_id:  # and parent_id in id_to_link:
            id_to_link[parent_id]["children"].append(link)

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
