from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.panels import FieldRowPanel, FieldPanel
from wagtail.embeds import blocks as embed_blocks
from wagtail.fields import StreamField
from wagtail.models import Page

import cmspage.blocks as cmsblocks
from cmspage.mixins import CMSTemplateMixin


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
        return self.find_existing_template(template_name, *self.template_styles)

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
        context["page_footer"] = CMSFooterPage.objects.live().first()

        # Prefetch images for all blocks to avoid N+1 queries
        if self.body:
            self._prefetch_block_images()

        return context

    def _prefetch_block_images(self):
        """Prefetch all images used in StreamField blocks to avoid N+1 queries"""
        image_ids = []

        # Helper function to recursively extract image IDs from blocks
        def _extract_image_ids(block):
            ids = []
            # If the block is a StructBlock or StreamBlock, recurse into its children
            if hasattr(block, "block") and hasattr(block.block, "child_blocks"):
                for child_name, child_block in block.block.child_blocks.items():
                    value = block.value.get(child_name)
                    if isinstance(value, list):
                        for item in value:
                            ids.extend(_extract_image_ids(item))
                    elif value is not None:
                        ids.extend(_extract_image_ids(value))
            # If the block is a StreamValue (list of blocks)
            elif isinstance(block, list):
                for item in block:
                    ids.extend(_extract_image_ids(item))
            # If the block contains an image id, extract it (assuming a convention)
            elif hasattr(block, "id"):
                ids.append(block.id)
            # If the block is a dict (raw value), check for image id keys
            elif isinstance(block, dict):
                for v in block.values():
                    ids.extend(_extract_image_ids(v))
            return ids

        for block in self.body:
            image_ids.extend(_extract_image_ids(block))

        if image_ids:
            # Deduplicate image_ids to avoid redundant queries
            deduped_image_ids = list(set(image_ids))
            # Prefetch all images with select_related to get both CMSPageImage and WagtailImage data
            from cmspage.models import CMSPageImage

            images = CMSPageImage.objects.filter(id__in=deduped_image_ids).select_related()
            # Store in a cache for template access
            self._prefetched_images = {img.id: img for img in images}

    @staticmethod
    def _extract_image_ids_from_block(block) -> list:
        """Extract image IDs from a block value"""
        image_ids = []
        block_type = block.block_type
        value = block.value

        # Handle different block types
        if block_type == "cards":
            image_ids.extend(card["image"].id for card in value.get("cards", []) if card.get("image"))
        elif block_type == "carousel":
            image_ids.extend(
                carousel_item["carousel_image"].id
                for carousel_item in value.get("carousel", [])
                if carousel_item.get("carousel_image")
            )
        elif block_type in ["image_and_text", "large_image"]:
            if value.get("image"):
                image_ids.append(value["image"].id)
        elif isinstance(value, dict) and value.get("image"):
            # Generic fallback for other image blocks
            image_ids.append(value["image"].id)

        return image_ids

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
