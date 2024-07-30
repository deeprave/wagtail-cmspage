from django.core.cache import cache
from django.http import HttpRequest
from wagtail.models import Site

from .models import SiteVariables, MenuLink


__all__ = ("navigation", "nav_pages_clear_cache")


NAV_CACHE_KEY_BASE = "nav"


def nav_pages_cache_key(site_id: int, user_id: int) -> str:
    return f"{NAV_CACHE_KEY_BASE}:{site_id}:{user_id}"


def nav_pages(request: HttpRequest):
    user_id = request.user.id if request.user.is_authenticated else 0
    site: Site = Site.find_for_request(request)
    cache_key = nav_pages_cache_key(site.id, user_id)
    pages = cache.get(cache_key)
    if pages is None:
        pages = MenuLink.objects.filter(site=site)
        cache.set(cache_key, pages)
    return pages


def nav_pages_clear_cache():
    for key in cache.iter_keys(f"{NAV_CACHE_KEY_BASE}:*"):
        cache.delete(key)


def navigation(request: HttpRequest) -> dict:
    return {"nav": nav_pages(request)}


def sitevariables(request: HttpRequest) -> dict:
    site: Site = Site.find_for_request(request)
    site_vars, created = SiteVariables.objects.get_or_create(site=site, defaults={"site": site, "vars": {}})
    return {"site": site} | site_vars
