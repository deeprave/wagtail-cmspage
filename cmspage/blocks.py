# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from wagtail import blocks
from wagtail.blocks import ListBlock
from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.documents import blocks as document_blocks
from wagtail.images import blocks as image_blocks
from wagtail.contrib.table_block import blocks as table_blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.telepath import register

from .themes import Backgrounds, Palette, Opacities, Heights, Insets, SocialIcon

__all__ = (
    "AbstractLinesBlock",
    "BackgroundBlock",
    "CallToActionBlock",
    "CardsBlock",
    "CarouselImageBlock",
    "CarouselImageStructBlock",
    "CopyrightBlock",
    "CustomTableBlock",
    "HeroImageBlock",
    "LargeImageBlock",
    "LineItemBlock",
    "LinesBlock",
    "LinkBlock",
    "LinksBlock",
    "NewSectionBlock",
    "RadioSelectBlock",
    "RichTextWithTitleBlock",
    "ImageAndTextBlock",
    "SmallImageAndTextBlock",
    "SocialLinkBlock",
    "SocialsBlock",
    "TitleBlock",
)

DEFAULT_RICHTEXTBLOCK_FEATURES = [
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "bold",
    "italic",
    "ol",
    "ul",
    "hr",
    "link",
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
    class Meta:
        label = "Background"
        form_template = "blocks/background_block.html"


class TitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    text = blocks.CharBlock(help_text="Title text to display")

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


class LinksBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Cards palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=255,
        label="links Title",
        help_text="Bold title text for this set of links (len=255)",
    )
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = "blocks/links_block.html"
        icon = "link"
        label = "Set of Links"


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


class SmallImageAndTextBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="CTA palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    title = blocks.CharBlock(max_length=60, required=False, blank=True, null=True)
    text = blocks.RichTextBlock(
        blank=True,
        required=False,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
    )
    image_alignment = RadioSelectBlock(
        choices=(
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),
        default="left",
        help_text="Image left - text right, or image right - text left.",
    )

    class Meta:
        template = "blocks/small_image_and_text_block.html"
        icon = "image"
        label = "Image & Text"


class ImageAndTextBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="CTA palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    title = blocks.CharBlock(max_length=60, required=False, blank=True, null=True)
    text = blocks.RichTextBlock(
        blank=True,
        required=False,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
    )
    image_alignment = RadioSelectBlock(
        choices=(
            ("full", "Full width centered"),
            ("left", "Image to the left"),
            ("right", "Image to the right"),
        ),
        default="full",
        help_text="Full image - text below, Image left - text right, or image right - text left.",
    )
    overlay = blocks.BooleanBlock(default=False, required=False, blank=True, help_text="Overlay text on image")

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
        icon = "warning"
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
        icon = "collapse-down"
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

    Methods:
        None

    """

    RICHTEXTBLOCK_FEATURES = ["bold", "italic", "ol", "ul", "usefont"]

    # noinspection PyUnresolvedReferences
    carousel_image = ImageChooserBlock()
    carousel_title = blocks.CharBlock(required=False, max_length=120, help_text="Display title, optional (max len=120)")
    carousel_content = blocks.RichTextBlock(required=False, features=RICHTEXTBLOCK_FEATURES, max_length=256, help_text="Short description")
    carousel_attribution = blocks.CharBlock(required=False, max_length=80, help_text="Attribution, optional (max len=80)")


class CarouselImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    carousel_interval = blocks.IntegerBlock(default=12000, help_text="Keep visible for time in milliseconds",)
    carousel = ListBlock(CarouselImageStructBlock())

    class Meta:
        template = "blocks/carousel_block.html"
        icon = "image"
        label = "Carousel"


class LineItemBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, help_text="Line text (max len=120)")
    content = blocks.RichTextBlock(required=False, features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Dropdown text block, optional")

    class Meta:
        template = "blocks/ålineitem_block.html"
        icon = "arrow-down"
        label = "Line Content"


class AbstractLinesBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="LineBlock palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    subtitle = blocks.CharBlock(required=False, help_text="Lines Title (optional)")
    number = blocks.BooleanBlock(required=False, default=False, help_text="Add number to lines")
    dropdown = blocks.BooleanBlock(required=False, default=False, help_text="Dropdown text (accordian)")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        context["uid"] = f"{id(self)}L"
        return context

    class Meta:
        abstract = True


class LinesBlock(AbstractLinesBlock):
    lines = blocks.ListBlock(LineItemBlock())

    class Meta:
        template = "blocks/lines_block.html"
        icon = "bars"
        label = "List of Lines"


class CopyrightBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="LineBlock palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    copyright = blocks.CharBlock(help_text="Copyright notice to display in the footer")

    def clean(self, value):
        cr = value.get("copyright")
        if "(c)" in cr:
            cr.replace("(c)", "©")
        value["copyright"] = cr
        return super().clean(value)

    class Meta:
        template = "blocks/copyright_block.html"
        icon = "success"
        label = "Copyright Notice"


URI_PATTERN = (
    r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:/{0,3}[a-zA-Z0-9.-]+(?:/?|[/?]\S*)"
    r"|mailto:[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
)

class SocialLinkBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(
        choices=SocialIcon.choices, default=SocialIcon.EMAIL, help_text="Social media icon"
    )
    name = blocks.CharBlock(max_length=120, help_text="Social media name")
    url = blocks.RegexBlock(URI_PATTERN, help_text="Social media URL")

    class Meta:
        template = "blocks/social_link_block.html"
        icon = "link"
        label = "Social Link"

class SocialLinkBlockAdapter(StructBlockAdapter):
    js_constructor = "cmspage.blocks.SocialLinkBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js=structblock_media._js + ["js/social-link-block.js"],
            css=structblock_media._css,
        )

register(SocialLinkBlockAdapter(), SocialLinkBlock)


class SocialsBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="LineBlock palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    links = blocks.ListBlock(SocialLinkBlock())

    class Meta:
        template = "blocks/socials_block.html"
        icon = "site"
        label = "Social Links"
