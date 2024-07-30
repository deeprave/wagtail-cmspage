from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.forms import forms
from wagtail.snippets.models import register_snippet
from wagtail import hooks

from .views import CarouselImageSnippetViewSet, MenuLinkViewSet, EventSnippetViewSet, SiteVariablesViewSet

register_snippet(CarouselImageSnippetViewSet)

register_snippet(MenuLinkViewSet)

register_snippet(SiteVariablesViewSet)

register_snippet(EventSnippetViewSet)

@hooks.register("construct_site_form")
def construct_site_form(request, form):
    if request.user.is_superuser:
        form.fields["variables__vars"] = forms.JSONField(
            widget=forms.JSONField,
            required=False,
            help_text="Enter site variables as JSON (e.g., {'key': 'value'})"
        )
    return form

@hooks.register("construct_site_panels")
def construct_site_panels(request, site, panels):
    if request.user.is_superuser:
        panels.append(
            MultiFieldPanel(
                [
                    FieldPanel("variables__vars"),
                ],
                heading="Site Variables",
                classname="collapsible",
            )
        )
    return panels
