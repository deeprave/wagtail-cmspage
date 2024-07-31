# -*- coding: utf-8 -*-
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import Tag as TaggitTag
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, FieldRowPanel, PageChooserPanel, MultiFieldPanel
from wagtail.admin.widgets import AdminPageChooser
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page, Site
from wagtail.snippets.models import register_snippet
from wagtail.images import get_image_model

from . import blocks as cmsblocks
from .mixins import CMSTemplateMixin

__all__ = (
    "CMSPage",
    "CMSHomePage",
    "SiteVariables",
)


class PageTag(TaggedItemBase):
    content_object = ParentalKey("cmspage.CMSPage", on_delete=models.CASCADE, related_name="cmspage_tags")


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
        MultiFieldPanel(
            [
                FieldPanel("seo_title"),
                FieldPanel("seo_keywords"),
            ],
            heading="Search Engine Optimisation",
        ),
    ] + Page.promote_panels

    class Meta:
        abstract = True


THERE_CAN_BE_ONLY_ONE = "Please select only one type of link: Page, Document or External Link."
NOT_A_MENU_PAGE = "The selected page is not marked to show in menus."


def min_length_validator(value):
    if len(value) < 2:
        raise ValidationError("Value must be at least 2 characters in length")


class MyPageChooser(AdminPageChooser):
    pass


class MenuLinkManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("link_page", "link_document")


class MenuLink(models.Model):
    """
    A class that represents a menu link.
    This is a standard django module that can be managed in the admin interface.

    Attributes:
        parent_pg (ParentalKey): A foreign key to the CMSPage model, to link to the page
        link_title (CharField): The title of the link.
        link_url (URLField): The URL of the link.
        link_order (IntegerField): The order of the link in the menu.

    Methods:
        None

    """

    site = models.ForeignKey(
        Site,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="+",
        default=getattr(settings, "SITE_ID", 1),
        help_text="Select the site to which the menu link applies",
    )
    menu_order = models.IntegerField("Order", default=0)
    menu_title = models.CharField("Menu Title", validators=[min_length_validator], max_length=32, default="Placeholder")
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Select Page",
        help_text="Select an internal page to link (leave blank for custom URL or document)",
    )
    link_document = models.ForeignKey(
        "wagtaildocs.Document",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Select Document",
        help_text="Select a document to link (leave blank for internal page or custom URL)",
    )
    link_url = models.URLField(
        "External Link",
        blank=True,
        help_text="Set a custom URL if not linking to a page or document",
    )

    def menu_site(self, _=None):
        return f"{self.site.site_name[:32]}{' (default)' if self.site.is_default_site else ''}"

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
    def url(self):
        if self.link_page:
            return self.link_page.url
        return self.link_document.url if self.link_document else self.link_url

    @staticmethod
    def get_cached_menu_links(site: Site, user_id: int):
        cache_key = f"menu_links:{site.id}:{user_id}"
        menu_links = cache.get(cache_key)
        if menu_links is None:
            menu_links = list(MenuLink.objects.filter(site=site).order_by("menu_order", "id"))
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

    objects = MenuLinkManager()

    class Meta:
        verbose_name = "Menu Link"
        ordering = ["menu_order", "id"]

    panels = [
        FieldPanel("site"),
        FieldRowPanel([FieldPanel("menu_title"), FieldPanel("menu_order")]),
        FieldRowPanel(
            [
                PageChooserPanel("link_page"),
                FieldPanel("link_document"),
            ]
        ),
        FieldPanel("link_url"),
    ]


class CarouselImage(Orderable):
    """
    A class that represents an image in a carousel.

    Attributes:
        RICHTEXTBLOCK_FEATURES (list): A list of rich text block features.
        Parent_pg (ParentalKey): A foreign key to the CMSPage model, to link to the page
        carousel_image (ForeignKey): A foreign key to each image.
        Carousel_title (CharField): The display title of the image.
        Carousel_content (RichTextField): Rich text content.
        Carousel_attribution (CharField): Attribution of the image.
        Carousel_interval (IntegerField): The interval of time the image is visible in milliseconds.

    Methods:
        None

    """

    RICHTEXTBLOCK_FEATURES = ["bold", "italic", "ol", "ul"]

    parent_pg = ParentalKey("cmspage.CMSPage", related_name="carousel_images")
    # noinspection PyUnresolvedReferences
    carousel_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    carousel_title = models.CharField(
        blank=True,
        null=True,
        max_length=120,
        help_text="Display title, optional (max len=120)",
    )
    carousel_content = RichTextField(features=RICHTEXTBLOCK_FEATURES, null=True, blank=True)
    carousel_attribution = models.CharField(
        blank=True,
        null=True,
        max_length=120,
        help_text="Display title, optional (max len=120)",
    )
    carousel_interval = models.IntegerField(
        blank=False,
        null=False,
        default=12000,
        help_text="Keep visible for time in milliseconds",
    )

    panels = [
        FieldPanel("carousel_image"),
        FieldPanel("carousel_title"),
        FieldPanel("carousel_content"),
        FieldPanel("carousel_attribution"),
        FieldPanel("carousel_interval"),
    ]


class EventManager(models.Manager):
    """
    Summary:
    - Provides methods to filter past and future events.

    Explanation:
    - This class provides methods to filter past and future events based on event date, time, and cancellation status.

    Args:
    - self: The EventManager instance.

    Returns:
    - QuerySet: A QuerySet of past or future events based on the filter criteria.
    """

    def past_events(self):
        return self.past_events_all().filter(event_cancelled=False)

    def past_events_all(self):
        now = timezone.now()
        return self.filter(event_datetime__lt=now)

    def future_events(self):
        return self.future_events_all().filter(event_cancelled=False)

    def future_events_all(self):
        now = timezone.now() - timedelta(hours=max(self.values_list("event_duration", flat=True)))
        return self.filter(event_datetime__ge=now)


class Event(models.Model):
    """
    A class that represents an event.

    Attributes:
        event_datetime (DateTimeField): The date and time of the event.
        Event_duration (FloatField): The expected duration of the event in hours.
        Event_title (CharField): The title of the event.
        Event_venue (CharField): The location of the event.
        Event_description (RichTextField): A long description of the event.
        Event_cancelled (BooleanField): A boolean field to indicate if the event has been cancelled.
    """

    event_datetime = models.DateTimeField("Event Date Time", db_index=True)
    event_duration = models.FloatField("Event Duration (hours)", default=1.0, validators=[MinValueValidator(0.0)])
    event_title = models.CharField(max_length=120)
    event_venue = models.TextField(max_length=120)
    event_description = RichTextField(features=["bold", "italic", "ol", "ul"])
    event_cancelled = models.BooleanField(default=False)

    objects = EventManager()

    @staticmethod
    def get_cached_events():
        today = timezone.now().date()
        cache_key = f"future_events:{today}"
        cached_events = cache.get(cache_key)
        if cached_events is None:
            cached_events = list(Event.objects.future_events())
            cache.set(cache_key, cached_events, 3600)
        return cached_events

    def __str__(self):
        return f"Event {self.event_title} at {self.event_venue} on {self.event_date} at {self.event_time}"

    class Meta:
        ordering = ["event_datetime"]


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
        ("video", cmsblocks.VideoBlock()),
        ("large_image", cmsblocks.LargeImageBlock()),
        ("table", cmsblocks.CustomTableBlock()),
        # utilities
        ("carousel", cmsblocks.CarouselImageBlock()),
        ("new_section", cmsblocks.NewSectionBlock()),
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


class CMSHomePage(CMSPage):
    page_description = "This page type is only for a site home page."
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["cmspage.CMSPage", "wagtailcore.Page"]
    max_count = 1

    class Meta:
        verbose_name = "CMS Home Page"
        verbose_name_plural = "CMS Home Pages"
