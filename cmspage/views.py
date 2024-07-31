from wagtail.admin.panels import FieldPanel
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import CarouselImage, MenuLink, SiteVariables, Event


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
    list_display = ["menu_site", "title", "menu_link", "menu_order"]


class SiteVariablesViewSet(SnippetViewSet):
    model = SiteVariables
    menu_label = "Site Variables"
    menu_icon = "cog"
    list_display = ("site",)
    list_filter = ("site",)  # Optional: Filter by site

    # def get_form_fields_for_edit(self):  # Override for custom form fields
    #     return {
    #         "vars": forms.JSONField(
    #             widget=forms.JSONField, help_text='Enter site variables as JSON (e.g., {"key": "value"})'
    #         )
    #     }


class EventSnippetViewSet(SnippetViewSet):
    model = Event
    list_display = ["event_datetime", "event_title", "event_duration"]
    list_filter = ["event_cancelled"]
    search_fields = ["event_title", "event_description"]
    ordering = ["event_datetime"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.GET.get("event_cancelled", False):
            queryset = queryset.filter(event_cancelled=True)
        return queryset
