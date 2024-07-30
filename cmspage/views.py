from wagtail.admin.panels import FieldPanel
from wagtail.forms import forms
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
    list_display = ["menu_title", "menu_link", "menu_order", "menu_site"]


class SiteVariablesViewSet(SnippetViewSet):
    model = SiteVariables
    menu_label = "Site Variables"
    menu_icon = "cog"
    list_display = ("site",)
    list_filter = ("site",)  # Optional: Filter by site

    def get_form_fields_for_edit(self):  # Override for custom form fields
        return {
            "vars": forms.JSONField(
                widget=forms.JSONField, help_text="Enter site variables as JSON (e.g., {'key': 'value'})"
            )
        }


class EventSnippetViewSet(SnippetViewSet):
    model = Event
    list_display = ["event_title", "event_date", "event_time", "event_hours"]
    list_filter = ["event_canceled"]
    search_fields = ["event_title", "event_description"]
    ordering = ["event_date", "event_time"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.GET.get("event_canceled", False):
            queryset = queryset.filter(event_canceled=False)
        return queryset
