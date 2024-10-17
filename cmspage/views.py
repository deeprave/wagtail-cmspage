from wagtail.models import Site
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import MenuLink, SiteVariables


class MenuLinkViewSet(SnippetViewSet):
    model = MenuLink
    icon = "link"  # Icon for the menu in Wagtail admin
    add_to_admin_menu = True
    menu_label = "Menu Links"
    menu_icon = "list-ul"
    menu_order = 300
    list_display = ["title", "parent_link", "menu_order", "menu_link_type"]

    def get_queryset(self, request):
        site = Site.find_for_request(request)
        return MenuLink.objects.get_ordered_queryset(site)


class SiteVariablesViewSet(SnippetViewSet):
    model = SiteVariables
    menu_label = "Site Variables"
    menu_icon = "cog"
    list_display = ("site",)
    list_filter = ("site",)  # Optional: Filter by site
