from wagtail import blocks
from wagtail.images import blocks as image_blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .radio import RadioSelectBlock
from .background import BackgroundBlock
from .themes import Palette, Insets, Justifications


class SmallImageAndTextBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="CTA palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    title = blocks.CharBlock(max_length=60, required=False, blank=True, null=True)
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
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
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
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


class LargeImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/large_image_block.html"
