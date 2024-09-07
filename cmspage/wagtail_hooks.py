from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.forms import forms
from wagtail.snippets.models import register_snippet
from wagtail import hooks

from .views import CarouselImageSnippetViewSet, MenuLinkViewSet, SiteVariablesViewSet


register_snippet(CarouselImageSnippetViewSet)

register_snippet(MenuLinkViewSet)

register_snippet(SiteVariablesViewSet)


@hooks.register("construct_site_form")
def construct_site_form(request, form):
    if request.user.is_superuser:
        form.fields["variables__vars"] = forms.JSONField(
            widget=forms.JSONField,
            required=False,
            help_text="""Enter site variables in JSON format (e.g., {"key1": "value1", "key2": "value2"})""",
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
