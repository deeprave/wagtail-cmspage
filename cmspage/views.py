from wagtail.admin.panels import FieldPanel
from wagtail.models import Site
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import CarouselImage, MenuLink, SiteVariables


class CarouselImageSnippetViewSet(SnippetViewSet):
    model = CarouselImage
    icon = "image"
    add_to_admin_menu = True
    menu_label = "Carousel Images"
    menu_icon = "image"
    menu_order = 400
    list_display = ["parent_pg", "carousel_title", "carousel_image"]
    search_fields = ("parent_pg", "carousel_title", "carousel_image")

    panels = [
        FieldPanel("parent_pg"),
        FieldPanel("carousel_title"),
        FieldPanel("carousel_image"),
    ]


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
