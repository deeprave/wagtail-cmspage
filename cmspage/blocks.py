# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.blocks import ListBlock
from wagtail.documents import blocks as document_blocks
from wagtail.images import blocks as image_blocks
from wagtail.embeds import blocks as embed_blocks
from wagtail.contrib.table_block import blocks as table_blocks
from wagtail.images.blocks import ImageChooserBlock

from .themes import Backgrounds, Palette, Opacities

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

class Heights(models.TextChoices):
    SMALLEST = "height-0", "None"
    SMALL = "height-1 py-1", "Small"
    MEDIUM = "height-2 py-2", "Medium"
    LARGE = "height-3 py-3", "Large"
    LARGER = "height-4 py-4", "Larger"
    LARGEST = "height-5 py-5", "Largest"


class Insets(models.TextChoices):
    SMALLEST = "p-0", "None"
    SMALL = "p-1", "Small"
    MEDIUM = "p-2", "Medium"
    LARGE = "p-3", "Large"
    LARGER = "p-4", "Larger"
    LARGEST = "p-5", "Largest"


class Meta:
    label = "Background"
    form_template = "blocks/background_block.html"

    class Meta:
        label = "Background"
        template = "blocks/background_block.html"
        form_template = "blocks/background_block_form.html"
        form_classname = "struct-block"


class TitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
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
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Cards palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
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
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    cards = blocks.ListBlock(Card())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        numcards = len(value["cards"])
        context.update(
            {
                "numcards": numcards,
                "colspread": 12 if numcards < 2 else 6 if numcards == 2 else 4 if numcards == 3 else 3,
            }
        )
        return context

    class Meta:
        template = "blocks/cards_block.html"
        icon = "image"
        label = "Set of Cards"


class RadioSelectBlock(blocks.ChoiceBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)


class ImageAndTextBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
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
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="CTA palette"
    )
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
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
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
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=60,
        help_text="Max length of 60 characters, optional",
    )
    video = embed_blocks.EmbedBlock(max_width=1200, help_text="Video URL")
    text = blocks.RichTextBlock(
        required=False,
        blank=True,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        help_text="Call to action text, optional (max=200)",
    )

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["video_class"] = "img-fluid"
        return context

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"
        label = "Embed Video"


class HeroImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/hero_block.html"


class LargeImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/large_image_block.html"


class NewSectionBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    height = blocks.ChoiceBlock(
        choices=Heights.choices, default=Heights.MEDIUM, help_text="Vertical space height"
    )

    class Meta:
        template = "blocks/new_section.html"
        icon = "horizontalrule"
        label = "Vertical space"


class CustomTableBlock(table_blocks.TableBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    class Meta:
        template = "blocks/custom_table_block.html"
        label = "Table"
        icon = "table"
        help_text = "Tabular data"


class CarouselImageStructBlock(blocks.StructBlock):
    """
    A class that represents an image in a carousel.

    Attributes:
        RICHTEXTBLOCK_FEATURES (list): A list of rich text block features.
        carousel_image (ForeignKey): A foreign key to each image.
        carousel_title (CharField): The display title of the image.
        carousel_content (RichTextField): Rich text content.
        carousel_attribution (CharField): Attribution of the image.
        carousel_interval (IntegerField): The interval of time the image is visible in milliseconds.

    Methods:
        None

    """

    RICHTEXTBLOCK_FEATURES = ["bold", "italic", "ol", "ul", "usefont"]

    # noinspection PyUnresolvedReferences
    carousel_image = ImageChooserBlock(required=True)
    carousel_title = blocks.CharBlock(required=False, max_length=120, help_text="Display title, optional (max len=120)")
    carousel_content = blocks.RichTextBlock(required=False, features=RICHTEXTBLOCK_FEATURES, max_length=256, help_text="Short description")
    carousel_attribution = blocks.CharBlock(required=False, max_length=80, help_text="Attribution, optional (max len=80)")


class CarouselImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    carousel_interval = blocks.IntegerBlock(required=True, default=12000, help_text="Keep visible for time in milliseconds",)
    carousel = ListBlock(CarouselImageStructBlock())

    class Meta:
        template = "blocks/carousel_block.html"
        icon = "image"
        label = "Carousel"
