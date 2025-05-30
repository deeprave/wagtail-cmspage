# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from wagtail.admin.panels import FieldPanel, FieldRowPanel, PageChooserPanel, MultiFieldPanel
from wagtail.admin.widgets import AdminPageChooser
from wagtail.models import Site, PreviewableMixin, DraftStateMixin, RevisionMixin
from wagtail.search.index import Indexed, FilterField, SearchField

from .choice_icon import IconChoices
from ..blocks import IconColorChoices


THERE_CAN_BE_ONLY_ONE = "Please select only one type of link: Page, Document or External Link."
NOT_A_MENU_PAGE = "The selected page is not marked to show in menus."
EXTERNAL_URL_REQUIRES_TITLE = "External URL requires a title."


def min_length_validator(value):
    if len(value) < 2:
        raise ValidationError("Value must be at least 2 characters in length")


class MyPageChooser(AdminPageChooser):
    pass


class MenuLinkManager(models.Manager):
    def _get_ordered_menu_links(self, site, parent=None, menu_links=None, ordered_links=None):
        if ordered_links is None:
            ordered_links = []
        if menu_links is None:
            menu_links = list(self.get_queryset().filter(site=site).order_by("menu_order", "id"))

        children = [link for link in menu_links if link.parent_id == parent]
        for child in children:
            ordered_links.append(child)
            self._get_ordered_menu_links(site, child.id, menu_links, ordered_links)

        return ordered_links

    def get_ordered_queryset(self, site: Site):
        # For each site, fetch the MenuLink records in the desired hierarchical order
        final_ordered_links = self._get_ordered_menu_links(site)

        # Extract IDs from the ordered links and construct an ordered queryset
        ordered_ids = [link.id for link in final_ordered_links]
        return (
            super()
            .get_queryset()
            .filter(id__in=ordered_ids)
            .order_by(models.Case(*[models.When(id=pk, then=pos) for pos, pk in enumerate(ordered_ids)]))
        )


class MenuLink(PreviewableMixin, DraftStateMixin, RevisionMixin, Indexed, models.Model):
    """
    A class that represents a menu link.
    This is a standard django module that can be managed in the admin interface.

    Attributes:
        parent (ParentalKey): A foreign key to the CMSPage model, to link to the page
        menu_title (CharField): The title of the link.
        menu_order (IntegerField): The order of the link in the menu.
        link_url (URLField): The URL of the link.

    Methods:
        None

    """

    cache_enabled = not settings.DEBUG

    site = models.ForeignKey(
        Site,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="+",
        default=getattr(settings, "SITE_ID", 1),
        help_text="Select the site to which the menu link applies",
    )
    parent = models.ForeignKey(
        "self",
        to_field="id",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Select a parent link to add it to a sub-menu, or blank for a top-level menu item",
    )
    menu_order = models.IntegerField("Order", default=0, help_text="Specify the order in the menu")
    menu_title = models.CharField(
        "Menu Title",
        validators=[min_length_validator],
        max_length=32,
        null=True,
        blank=True,
        help_text="Override the menu title",
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="menu_links",
        verbose_name="Select Page",
        help_text=(
            "Select an internal page to link (leave blank for custom URL or document)."
            "Leave title blank to use this page's title"
        ),
    )
    link_document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Select Document",
        help_text=(
            "Select a document to link (leave blank for internal page or custom URL)."
            "Leave title blank to use this document's title"
        ),
    )
    # don't use URLField because it doesn't allow an empty scheme for self-site references
    link_url = models.CharField(
        "External Link",
        blank=True,
        help_text="Set a custom URL if not linking to a page or document." "Title is required for this link type",
    )
    menu_icon = models.CharField(
        "Icon",
        choices=IconChoices.choices,
        default=IconChoices.NONE,
        max_length=64,
        blank=True,
        help_text="Select an icon to display next to the link",
    )
    menu_icon_color = models.CharField(
        "Icon Color",
        choices=IconColorChoices.choices,
        default=IconColorChoices.BODY,
        max_length=16,
        blank=True,
        help_text="Specify a theme color for the icon",
    )
    staff_only = models.BooleanField(
        "Staff Only",
        default=False,
        help_text="Check this box to restrict display to staff users only",
    )
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="menu_links")

    objects = MenuLinkManager()

    def get_preview_context(self, request, mode_name):
        from cmspage.models import CMSFooterPage
        return {
            "level": 0,
            "navigation": self.get_menu_links(self.site),
            "page_footer": CMSFooterPage.objects.first(),
            "include": {
                "header": "cmspage/includes/header.html",
                "messages": "cmspage/includes/messages.html",
                "main": "cmspage/includes/main.html",
                "footer": "cmspage/includes/footer.html",
                "navigation": "cmspage/includes/navigation.html",
                "navigation_item": "cmspage/includes/navigation_item.html",
            }
        }

    def get_preview_template(self, request, mode_name):
        return "preview/menu_link.html"

    def menu_site(self, _=None):
        return f"{self.site.site_name}{' (default)' if self.site.is_default_site else ''}"

    @property
    def title(self):
        return self.menu_title or self.menu_link_title

    @property
    def menu_link_title(self, _=None):
        if self.link_page:
            return self.link_page.title
        return self.link_document.title if self.link_document else self.link_url

    @property
    def menu_link_type(self, _=None):
        if self.link_page:
            return "Page"
        return "Document" if self.link_document else "URL"

    @property
    def menu_link_icon(self, _=None):
        return self.menu_icon

    @property
    def parent_link(self):
        return self.parent or ""

    @property
    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_document.url if self.link_document else self.link_url

    @classmethod
    def get_menu_links(cls, site: Site):
        return list(MenuLink.objects.get_ordered_queryset(site))

    MENU_LINKS_KEY = "menu_links_ids"
    MENU_LINKS_TIMEOUT = 1800  # 30 minutes

    @classmethod
    def get_cached_menu_links(cls, site: Site, user_id: int):
        if not cls.cache_enabled:
            return cls.get_menu_links(site)

        cache_key = f"menu_links:{site.id}:{user_id}"
        menu_links = cache.get(cache_key)
        if menu_links:
            return menu_links
        menu_links = cls.get_menu_links(site)
        cache.set(cache_key, menu_links, cls.MENU_LINKS_TIMEOUT)

        # get and update the list of cached site.id/user_id combos
        # this simplifies deletion of cached menu links
        registry = cache.get(cls.MENU_LINKS_KEY) or set()
        registry.add((site.id, user_id))
        cache.set(cls.MENU_LINKS_KEY, registry, cls.MENU_LINKS_TIMEOUT)

        return menu_links

    @classmethod
    def clear_cached_menu_links(cls):
        registry = cache.get(cls.MENU_LINKS_KEY) or set()

        for site_id, user_id in registry:
            if site_id and user_id:  # Basic validation
                cache_key = f"menu_links:{site_id}:{user_id}"
                cache.delete(cache_key)

        # Delete the registry itself
        cache.delete(cls.MENU_LINKS_KEY)

    def clean(self):
        super().clean()
        num_selected = bool(self.link_page) + bool(self.link_document) + bool(self.link_url)
        if num_selected != 1:
            raise ValidationError(
                {
                    "link_page": ValidationError(THERE_CAN_BE_ONLY_ONE),
                    "link_document": ValidationError(THERE_CAN_BE_ONLY_ONE),
                    "link_url": ValidationError(THERE_CAN_BE_ONLY_ONE),
                }
            )
        elif self.link_page and not self.link_page.show_in_menus:
            raise ValidationError({"link_page": ValidationError(NOT_A_MENU_PAGE)})
        elif self.link_url and not self.menu_title:
            raise ValidationError({"link_url": ValidationError(EXTERNAL_URL_REQUIRES_TITLE)})

    def __str__(self):
        return self.title

    class Meta:
        app_label = "cmspage"
        verbose_name = "Menu Link"
        ordering = ["menu_order", "id"]

    panels = [
        FieldPanel("site"),
        FieldPanel("parent"),
        MultiFieldPanel(
            [
                PageChooserPanel("link_page"),
                FieldPanel("link_document"),
                FieldPanel("link_url"),
            ],
            heading="Link To",
        ),
        MultiFieldPanel(
            [
                FieldPanel("menu_title"),
                FieldRowPanel([FieldPanel("menu_icon"), FieldPanel("menu_icon_color"), FieldPanel("menu_order")]),
            ],
        ),
    ]

    search_fields = [
        FilterField("title"),
        FilterField("parent"),
        SearchField("title"),
        SearchField("url"),
    ]

@receiver([post_save, post_delete], sender=MenuLink)
def clear_menu_link_cache(sender, instance, **kwargs):
    """
    Clear the MenuLink cache whenever a MenuLink is saved or deleted.
    """
    MenuLink.clear_cached_menu_links()
