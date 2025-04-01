from collections import defaultdict
import logging
from functools import cache
from typing import List

from django.http import HttpRequest
from django.contrib.auth import get_user_model
from wagtail.models import Site

from .models import MenuLink

__all__ = ("navigation", "cmspage_context")

User = get_user_model()
logger = logging.getLogger("cmspage.context_processors")

centering = "-c50"

@cache
def image_config(_: HttpRequest):
    """Provide image configurations for templates."""

    # Define base dimensions as tuples (width, height)
    base = {
        "portrait": {
            "tiny": (270, 480),
            "small": (360, 640),
            "medium": (540, 960),
            "large": (720, 1280),
            "full-width": (1080, 1920),
            "original": (None, None),
        },
        "landscape": {
            "tiny": (480, 270),
            "small": (640, 360),
            "medium": (960, 540),
            "large": (1280, 720),
            "full-width": (1920, 1080),
            "original": (None, None),
        }
    }

    # Build the complete dimensions dictionary
    image_dimensions = {}
    for orientation, sizes in base.items():
        image_dimensions[orientation] = {}
        for size, (width, height) in sizes.items():
            # Handle the special case for "original" size
            spec = size if size == "original" else f"fill-{width}x{height}{centering}"

            # Create the full configuration for this orientation/size
            image_dimensions[orientation][size] = {
                "width": width,
                "height": height,
                "spec": spec
            }

    # Define alignment classes mapping
    image_alignment = {
        "left": {"text": "text-start", "overlay": "overlay-text-right"},
        "right": {"text": "text-end", "overlay": "overlay-text-left"},
        "center": {"text": "text-center", "overlay": ""},
        "full": {"text": "", "overlay": "overlay-top"},
    }

    return {
        "image": {
            "dims": image_dimensions,
            "align": image_alignment,
        }
    }


def _nav_pages_for_site(site: Site, user: User|None) -> List[dict]:
    user_id = user.pk if user else 0
    cached_menu_links = MenuLink.get_cached_menu_links(site, user_id)

    tree = []
    id_to_link = {}
    unlinked = defaultdict(list)

    for link in cached_menu_links:
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


def cmspage_context(request: HttpRequest) -> dict:
    # combines all the above context processors into one
    return navigation(request) | image_config(request)
