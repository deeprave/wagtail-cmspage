from typing import List

from django.forms.models import model_to_dict
from django.http import HttpRequest
from wagtail.models import Site

from .models import SiteVariables, MenuLink, Event

__all__ = ("navigation", "events", "site_variables", "cmspage_context")


def _nav_pages_for_site(site: Site, user_id: int) -> List[dict]:
    return [
        {
            "title": link.menu_title or link.menu_link_title,
            "type": link.menu_link_type,
            "url": link.url,
        }
        for link in MenuLink.get_cached_menu_links(site, user_id)
    ]


def navigation(request: HttpRequest) -> dict:
    user_id = request.user.id if request.user.is_authenticated else 0
    site: Site = Site.find_for_request(request)
    return {"navigation": _nav_pages_for_site(site, user_id)}


def _get_events() -> List[dict]:
    return [model_to_dict(event) for event in Event.get_cached_events()]


def events(_: HttpRequest) -> dict:
    return {"events": _get_events()}


def site_variables(request: HttpRequest) -> dict:
    site: Site = Site.find_for_request(request)
    site_vars, _ = SiteVariables.get_cached_variables(site)
    return {"site": site} | site_vars


def cmspage_context(request: HttpRequest) -> dict:
    # combines all the above context processors into one
    return navigation(request) | events(request) | site_variables(request)
