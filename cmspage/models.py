# -*- coding: utf-8 -*-
import os

from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, FieldRowPanel, PageChooserPanel, MultiFieldPanel
from wagtail.admin.widgets import AdminPageChooser
from wagtail.embeds import blocks as embed_blocks
from wagtail.fields import StreamField
from wagtail.images.models import Image as WagtailImage
from wagtail.models import Page, Site
from wagtail.snippets.models import register_snippet
from PIL import Image as WillowImage

from .mixins import CMSTemplateMixin
from .choice_icon import IconChoices
from . import blocks as cmsblocks

__all__ = (
    "CMSPage",
    "CMSPageBase",
    "CMSHomePage",
    "SiteVariables",
    "MenuLink",
    "MenuLinkManager",
)


class PageTag(TaggedItemBase):
    content_object = ParentalKey("wagtailcore.Page", on_delete=models.CASCADE, related_name="cmspage_tags")


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class SiteVariables(models.Model):
    """

    SiteVariables Model

    This class represents the site variables model, which is used to store and manage
    custom variables for a specific site.

    Attributes:
        site (Site): The site associated with the variables.
        vars (dict): The dictionary of variables.
                     It is stored as a JSONField in the database.

    Meta:
        verbose_name (str): The human-readable name for the model.

    """

    site = models.OneToOneField(Site, on_delete=models.CASCADE, related_name="variables")
    vars = models.JSONField(blank=True, null=True, default=dict)

    @staticmethod
    def get_cached_variables(site: Site) -> dict:
        cache_key = f"site_variables:{site.id}"
        site_vars = cache.get(cache_key)
        if not site_vars:
            site_record = SiteVariables.objects.filter(site=site).first()
            site_vars = site_record.vars if site_record else {}
            cache.set(cache_key, site_vars, timeout=900)
        return site_vars

    @staticmethod
    def clear_cached_variables(site: Site):
        cache.delete(f"site_variables:{site.id}")

    class Meta:
        verbose_name = "Site Variables"


# This is optional but to activate this feature, you need to add the following to your settings.py
# in order to take advantage of converting images to WebP format when imported instead of when rendering the page.
# WAGTAILIMAGES_IMAGE_MODEL = 'cmspage.CMSPageImage'


class CMSPageImage(WagtailImage):
    def save(self, *args, **kwargs):
        # Call the original save method to save the image first
        super().save(*args, **kwargs)

        # Get the original image path
        original_image_path = self.file.path

        # Open the original image using PIL
        with WillowImage.open(original_image_path) as image:
            # Define the new path for the WebP image
            webp_image_path = f"{os.path.splitext(original_image_path)[0]}.webp"
            # Save the image in WebP format
            image.save(webp_image_path, "WEBP")

        # Optionally, update the file field to the new WebP path, if required
        self.file.name = f"{os.path.splitext(self.file.name)[0]}.webp"
        super().save(*args, **kwargs)  # Save again to update the file name


class AbstractCMSPage(Page, CMSTemplateMixin):
    """
    The `AbstractCMSPage` class handles the overall configurations for all Content Management System (CMS) pages.
     You can modify its behaviour by either overriding the class's properties or by adjusting the corresponding
     settings:

    - `CMSPAGE_STYLES`: A string containing styles, separated by either a comma or space that are used to look
      for templates. This setting provides flexibility in searching templates based on style or company branding.
    - `CMSPAGE_INCLUDE_PATH`: An identifier representing the path to the "include" templates.
      It defaults to "includes".
    - `CMSPAGE_INCLUDES`: Contains a list of include templates to search for.

    The interpretation of these settings in rendering templates is as follows:
    - **Page template pattern**: `<base_template_path>/[{cmspage_style1}.../]<template_name>[.html]`
       The base template path forms the root, following which it looks for template names in different CMS page
       styles (if provided). The exact template to be loaded is finally referenced by its name and `.html`
       extension (if present).
    - **Include names pattern**: `<base_template_path>/[{cmspage_style1}.../]<include_path>/<include_name>`
      Similar to the page template, it looks for includes in the possible CMS page styles directories under the
      base template path and the provided include path. The exact include file is then identified by its name.

    Note that non-existing templates specified in any of the settings will be ignored and variables for use
    in templates will be omitted.
    """

    default_template_dir = "cmspage"
    default_include_dir = "includes"

    def get_template(self, request, *args, **kwargs) -> str:
        template_name = super().get_template(request, *args, **kwargs)
        return self.find_existing_template(template_name, *self.template_styles)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["base_template"] = self.base_template
        context |= {"include": self.include_templates()}
        return context

    tags = ClusterTaggableManager(
        through="cmspage.PageTag",
        blank=True,
        help_text="Tags used to search for this page (optional)",
    )
    display_title = models.BooleanField(default=True, help_text="Display the page title on the page")
    display_tags = models.BooleanField(default=False, help_text="Display the page tags on the page")
    seo_keywords = models.CharField(max_length=255, blank=True, help_text="SEO Keywords")

    content_panels = [
        FieldRowPanel(
            [
                FieldPanel("title", heading="Page Title"),
                FieldPanel("display_title", heading="Display?", help_text="Check to display the title on the page"),
            ]
        ),
        FieldRowPanel(
            [
                FieldPanel("tags", heading="Page Tags (search and group)"),
                FieldPanel("display_tags", heading="Display?", help_text="Check to display tags on the page"),
            ]
        ),
    ]

    promote_panels = [
        FieldPanel("seo_title", heading="Seo title"),
        FieldPanel("seo_keywords"),
    ] + Page.promote_panels

    class Meta:
        abstract = True


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


class IconColorChoices(models.TextChoices):
    BODY = "text-body", "Normal"
    WHITE = "text-white", "White"
    BLACK = "text-black", "Dark"
    PRIMARY = "text-primary", "Primary"
    SECONDARY = "text-secondary", "Secondary"
    SUCCESS = "text-success", "Success"
    WARNING = "text-warning", "Warning"
    INFO = "text-info", "Info"
    DANGER = "text-danger", "Danger"
    LIGHT = "text-light", "Light"
    DARK = "text-dark", "Dark"
    MUTED = "text-muted", "Muted"
    BLACK50 = "text-black-50", "Black 50% opacity"
    WHITE50 = "text-white-50", "White 50% opacity"


class MenuLink(models.Model):
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
    link_url = models.URLField(
        "External Link",
        blank=True,
        help_text=("Set a custom URL if not linking to a page or document." "Title is required for this link type"),
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
    def get_cached_menu_links(cls, site: Site, user_id: int):
        cache_key = f"menu_links:{site.id}:{user_id}"
        menu_links = cls.cache_enabled and cache.get(cache_key)
        if not menu_links:
            menu_links = list(MenuLink.objects.get_ordered_queryset(site))
            cache.set(cache_key, menu_links, 300)
        return menu_links

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

    objects = MenuLinkManager()

    def __str__(self):
        return self.title

    class Meta:
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


class CMSPageBase(AbstractCMSPage):
    body_blocks = [
        # header
        ("hero", cmsblocks.HeroImageBlock(label="Hero Image", max_num=1)),
        ("title", cmsblocks.TitleBlock(label="Title", max_num=1)),
        # main content
        ("cards", cmsblocks.CardsBlock()),
        ("image_and_text", cmsblocks.ImageAndTextBlock()),
        ("cta", cmsblocks.CallToActionBlock()),
        ("richtext", cmsblocks.RichTextWithTitleBlock()),
        ("video", embed_blocks.EmbedBlock(max_with=1200, help_text="Video URL")),
        ("large_image", cmsblocks.LargeImageBlock()),
        ("table", cmsblocks.CustomTableBlock()),
        # utilities
        ("carousel", cmsblocks.CarouselImageBlock()),
        ("new_section", cmsblocks.NewSectionBlock()),
        ("lines", cmsblocks.LinesBlock()),
    ]

    body = StreamField(body_blocks, blank=True, null=True)

    class Meta:
        abstract = True

    content_panels = AbstractCMSPage.content_panels + [
        FieldPanel("body"),
    ]


class CMSPage(CMSPageBase):
    page_description = "This page type is for general content and can be used for most purposes."
    # Default implementation of CMSPage
    parent_page_types = ["cmspage.CMSHomePage", "cmspage.CMSPage"]
    subpage_types = ["cmspage.CMSPage", "wagtailcore.Page"]

    class Meta:
        verbose_name = "CMS Page"
        verbose_name_plural = "CMS Pages"


class CMSHomePage(CMSPageBase):
    page_description = "This page type is only for a site home page."
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["cmspage.CMSPage", "wagtailcore.Page"]
    max_count = 1

    body_blocks = [
        ("hero", cmsblocks.HeroImageBlock(label="Hero Image", max_num=1)),
    ] + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True, null=True)

    class Meta:
        verbose_name = "CMS Home Page"
        verbose_name_plural = "CMS Home Pages"
