# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from modelcluster.fields import ParentalManyToManyField
from wagtail import blocks
from wagtail.documents import blocks as document_blocks
from wagtail.images import blocks as image_blocks
from wagtail.embeds import blocks as embed_blocks
from wagtail.contrib.table_block import blocks as table_blocks

from .choice_bg import Backgrounds, Opacities

__all__ = (
    "LinkBlock",
    "CardsBlock",
    "RadioSelectBlock",
    "ImageAndTextBlock",
    "CallToActionBlock",
    "CustomTableBlock",
    "RichTextWithTitleBlock",
    "LargeImageBlock",
    "HeroImageBlock",
    "NewSectionBlock",
    "VideoBlock",
    "BackgroundBlock",
)

DEFAULT_RICHTEXTBLOCK_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "document-link",
    "image",
    "embed",
    "code",
    "blockquote",
    "superscript",
    "subscript",
    "strikethrough",
    "usefont",
]


class BackgroundBlock(blocks.StructBlock):
    background = blocks.ChoiceBlock(
        choices=Backgrounds.choices, default=Backgrounds.NONE, help_text="Background type or color"
    )
    opacity = blocks.ChoiceBlock(
        choices=Opacities.choices, default=Opacities.OPACITY_FULL, help_text="Background opacity"
    )


class TitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    text = blocks.CharBlock(required=True, help_text="Title text to display")

    class Meta:
        template = "blocks/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"


class LinkValue(blocks.StructValue):
    """
    Generates a URL and Title for blocks with multiple link choices.
    """

    @property
    def link_title(self):
        if not (title := self.get("title")):
            if not (title := self.get("button_title")):
                if not (title := self.get("page_link")):
                    if not (title := self.get("doc_link")):
                        title = self.get("extra_link").title
        return title

    @property
    def link_url(self):
        page_url = self.get("page_link").url if self.get("page_link") else None
        doc_url = self.get("doc_link").url if self.get("doc_link") else None
        extra_link = self.get("extra_link")
        if page_url and extra_link:
            return f"{page_url}{extra_link}"
        return page_url or doc_url or extra_link


ONE_LINK_ERROR_MESSAGE = "You must select a page or document, or enter an external link."
INVALID_LINK_ERROR_MESSAGE = "Invalid link. Please select a page or document, or enter a valid URL."


class LinkBlock(blocks.StructBlock):
    """
    Common attributes for creating a link within the CMS.
    """

    page_link = blocks.PageChooserBlock(
        required=False,
        label="Page link",
    )
    doc_link = document_blocks.DocumentChooserBlock(
        required=False,
        label="Document link",
    )
    extra_link = blocks.CharBlock(
        required=False,
        max_length=255,
        label="Extra link",
    )
    button_title = blocks.CharBlock(
        required=False,
        max_length=255,
        label="Button Title (use hyphen for special link button)",
    )

    def clean(self, value):
        errors = {}
        page_link = value.get("page_link")
        doc_link = value.get("doc_link")
        extra_link = value.get("extra_link")
        if sum((bool(page_link), bool(doc_link), bool(extra_link))) > 1:
            errors["page_link"] = ErrorList([ONE_LINK_ERROR_MESSAGE])
            errors["doc_link"] = ErrorList(["ONE_LINK_ERROR_MESSAGE"])
            errors["extra_link"] = ErrorList([ONE_LINK_ERROR_MESSAGE])

        if errors:
            raise ValidationError(INVALID_LINK_ERROR_MESSAGE, params=errors)
        return super().clean(value)

    class Meta:
        value_class = LinkValue


class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=255,
        label="Card Title",
        help_text="Bold title text for this card (len=255)",
    )
    text = blocks.RichTextBlock(
        blank=True, null=True, required=False, label="Card Text", help_text="Optional text for this card"
    )
    image = image_blocks.ImageChooserBlock(required=False, label="Card Image", help_text="Image (resized)")
    link = LinkBlock(required=False, label="Card Link", help_text="Enter a page or document, or an external link")


class CardsBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    cards = blocks.ListBlock(Card())

    class Meta:
        template = "blocks/cards_block.html"
        icon = "image"
        label = "Set of Cards"


class RadioSelectBlock(blocks.ChoiceBlock):
    bg = BackgroundBlock()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class ImageAndTextBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    image_alignment = RadioSelectBlock(
        choices=(
            ("full", "Full width centered"),
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),
        default="full",
        help_text="Full image - text below, Image left - text right, or image right - text left.",
    )
    image_size = RadioSelectBlock(
        choices=(
            ("standard", "Standard 786x552"),
            ("landscape", "Landscape 786x1104"),
            ("portrait", "Portrait 786x300"),
        ),
        default="standard",
        help_text="Layout - match with picture dimensions",
    )
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=60,
        help_text="Max length of 60 characters.",
    )
    text = blocks.RichTextBlock(
        blank=True,
        required=False,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        help_text="Description for this item",
    )
    overlay = blocks.BooleanBlock(default=False, required=False, blank=True, help_text="Overlay text on image")
    link = LinkBlock(required=False, blank=True, null=True)

    class Meta:
        template = "blocks/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"


class CallToActionBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=60,
        help_text="Max length of 60 characters, optional",
    )
    text = blocks.RichTextBlock(
        required=False,
        blank=True,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        help_text="Call to action text, optional (max=200)",
    )
    link = LinkBlock(required=False, blank=True, null=True)

    class Meta:
        template = "blocks/call_to_action_block.html"
        icon = "plus"
        label = "Call to Action"


class RichTextWithTitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=120,
        help_text="Display title, optional (max len=120)",
    )
    content = blocks.RichTextBlock(features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Rich text block, required")

    class Meta:
        template = "blocks/simple_richtext_block.html"
        label = "RichText with Title"
        icon = "doc-empty-inverse"


class VideoBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=60,
        help_text="Max length of 60 characters, optional",
    )
    video = embed_blocks.EmbedBlock()
    text = blocks.RichTextBlock(
        required=False,
        blank=True,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        help_text="Call to action text, optional (max=200)",
    )

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"
        label = "Embed Video"


class HeroImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/hero_block.html"


class LargeImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/large_image_block.html"


class NewSectionBlock(blocks.StaticBlock):
    bg = BackgroundBlock()

    class Meta:
        template = "blocks/new_section.html"
        icon = "horizontalrule"
        label = "Start new section"


class CustomTableBlock(table_blocks.TableBlock):
    bg = BackgroundBlock()

    class Meta:
        template = "blocks/custom_table_block.html"
        label = "Table"
        icon = "table"
        help_text = "Tabular data"


class CarouselImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    carousel = ParentalManyToManyField("cmspage.CarouselImage", blank=True)

    class Meta:
        template = "blocks/carousel_block.html"
        icon = "image"
        label = "Carousel"
