from collections import defaultdict
from collections.abc import Mapping

from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldRowPanel, FieldPanel
from wagtail.embeds import blocks as embed_blocks
from wagtail.fields import StreamField
from wagtail.images.models import AbstractImage
from wagtail.models import Page

import cmspage.blocks as cmsblocks
from cmspage.mixins import CMSTemplateMixin, log_template_debug


class AbstractCMSPage(CMSTemplateMixin, Page):
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
        resolved = CMSTemplateMixin.find_existing_template(template_name, *self.template_styles) or template_name
        log_template_debug(f"Resolved template: {resolved}")
        return resolved

    def get_context(self, request, *args, **kwargs):
        return super().get_context(request, *args, **kwargs)

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
        app_label = "cmspage"
        abstract = True


class CMSPageBase(AbstractCMSPage):
    body_blocks = [
        # header
        ("hero", cmsblocks.hero.HeroImageBlock(label="Hero Image", max_num=1)),
        ("title", cmsblocks.title.TitleBlock(label="Title", max_num=1)),
        # main content
        ("cards", cmsblocks.cards.CardsBlock()),
        ("image_and_text", cmsblocks.image_and_text.ImageAndTextBlock()),
        ("cta", cmsblocks.cta.CallToActionBlock()),
        ("richtext", cmsblocks.title.RichTextWithTitleBlock()),
        ("video", embed_blocks.EmbedBlock(max_with=1200, help_text="Video URL")),
        ("large_image", cmsblocks.image_and_text.LargeImageBlock()),
        ("table", cmsblocks.custom_table.CustomTableBlock()),
        # utilities
        ("carousel", cmsblocks.carousel.CarouselImageBlock()),
        ("new_section", cmsblocks.new_section.NewSectionBlock()),
        ("lines", cmsblocks.lines.LinesBlock()),
    ]

    body = StreamField(body_blocks, blank=True, null=True)

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        footer = CMSFooterPage.objects.live().first()
        context["page_footer"] = footer

        self._prefetch_stream_renditions(self.body)
        if footer is not None:
            self._prefetch_stream_renditions(footer.footer)

        return context

    @classmethod
    def _mapping(cls, value):
        return value if isinstance(value, Mapping) else {}

    @classmethod
    def _iter_images_from_block(cls, block):
        """Yield image instances referenced by a StreamField block."""
        if hasattr(block, "block_type"):
            value = block.value if hasattr(block, "value") else None
            mapping = cls._mapping(value)
            if block.block_type == "cards":
                for card in mapping.get("cards") or []:
                    image = cls._mapping(card).get("image")
                    if image is not None:
                        yield image
            elif block.block_type == "carousel":
                for item in mapping.get("carousel") or []:
                    image = cls._mapping(item).get("carousel_image")
                    if image is not None:
                        yield image
            else:
                image = mapping.get("image") or mapping.get("carousel_image")
                if image is not None and hasattr(image, "id"):
                    yield image

        elif isinstance(block, list):
            for item in block:
                yield from cls._iter_images_from_block(item)

        elif isinstance(block, AbstractImage):
            yield block

        elif isinstance(block, Mapping):
            image = block.get("image") or block.get("carousel_image")
            if image is not None and hasattr(image, "id"):
                yield image

    @classmethod
    def _extract_image_ids_from_block(cls, block):
        return [image.id for image in cls._iter_images_from_block(block) if getattr(image, "id", None)]

    @staticmethod
    def _attach_prefetched_renditions(images):
        """Copy renditions onto the StreamField image instances `{% image %}` will use."""
        instances = [image for image in images if image is not None and getattr(image, "id", None)]
        if not instances:
            return

        by_model = defaultdict(list)
        for image in instances:
            by_model[type(image)].append(image)

        for model, model_images in by_model.items():
            fetched = model.objects.filter(id__in={image.id for image in model_images}).prefetch_renditions()
            renditions_by_id = {image.id: image.prefetched_renditions for image in fetched}
            for image in model_images:
                renditions = renditions_by_id.get(image.id)
                if renditions is not None:
                    image.prefetched_renditions = renditions

    def _prefetch_stream_renditions(self, stream):
        if not stream:
            return
        images = []
        for block in stream:
            images.extend(self._iter_images_from_block(block))
        self._attach_prefetched_renditions(images)

    def _prefetch_block_images(self):
        self._prefetch_stream_renditions(self.body)

    class Meta:
        app_label = "cmspage"
        abstract = True

    content_panels = AbstractCMSPage.content_panels + [
        FieldPanel("body"),
    ]


class CMSPage(CMSPageBase):
    page_description = "This page type is for general content and can be used for most purposes."
    # Default implementation of CMSPage
    parent_page_types = ["cmspage.CMSHomePage", "cmspage.CMSPage"]
    subpage_types = ["cmspage.CMSPage", "wagtailcore.Page", "cmspage.CMSFormPage"]

    class Meta:
        app_label = "cmspage"
        verbose_name = "CMS Page"
        verbose_name_plural = "CMS Pages"


class CMSFooterPage(AbstractCMSPage):
    page_description = "This page type is for the site footer."
    max_count = 1

    footer_blocks = [
        ("info", cmsblocks.image_and_text.SmallImageAndTextBlock()),
        ("copy", cmsblocks.copy.CopyrightBlock(label="Copyright", classnames="text-center text-muted text-small")),
        ("links", cmsblocks.links.LinksBlock()),
        ("social", cmsblocks.social.SocialsBlock()),
        ("new_section", cmsblocks.new_section.NewSectionBlock()),
    ]
    footer = StreamField(footer_blocks, blank=False, null=False)

    content_panels = AbstractCMSPage.content_panels + [
        FieldPanel("footer"),
    ]

    class Meta:
        app_label = "cmspage"
        verbose_name = "CMS Footer Page"
        verbose_name_plural = "CMS Footer Pages"


class CMSHomePage(CMSPageBase):
    page_description = "This page type is only for a site home page."
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = ["cmspage.CMSPage", "wagtailcore.Page", "cmspage.CMSFooterPage", "cmspage.CMSFormPage"]
    max_count = 1

    body_blocks = [
        ("hero", cmsblocks.hero.HeroImageBlock(label="Hero Image", max_num=1)),
    ] + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True, null=True)

    class Meta:
        app_label = "cmspage"
        verbose_name = "CMS Home Page"
        verbose_name_plural = "CMS Home Pages"
