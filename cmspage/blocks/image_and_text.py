from wagtail import blocks
from wagtail.images import blocks as image_blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .radio import RadioSelectBlock
from .themes import Palette, Insets, Justifications, ImageAlignment, Orientations, ImageSizes, CropPercentage, \
    ImageRounding
from .links import LinkBlock


class SmallImageAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=60, required=False, blank=True, null=True)
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font on title?")
    text = blocks.RichTextBlock(
        blank=True,
        required=False,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
    )
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    orientation = blocks.ChoiceBlock(choices=Orientations.choices, default=Orientations.LANDSCAPE, help_text="Image orientation")
    size = blocks.ChoiceBlock(choices=ImageSizes.choices, default=ImageSizes.MEDIUM, help_text="Image size")
    crop = blocks.ChoiceBlock(choices=CropPercentage.choices, default=CropPercentage.FULL, help_text="Crop percentage")
    rounded = blocks.ChoiceBlock(choices=ImageRounding.choices, default=ImageRounding.NONE, help_text="Image rounding")
    responsive = blocks.BooleanBlock(required=False, default=False, help_text="Image responsive")
    image_alignment = RadioSelectBlock(
        choices=ImageAlignment.choices,
        default="left",
        help_text="Image left - text right, or image right - text left.",
    )
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    link = LinkBlock()

    class Meta:
        template = "blocks/small_image_and_text_block.html"
        icon = "image"
        label = "Small Image & Text"
        label_format = "Small Image & Text {title}"


class ImageAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=60, required=False, blank=True, null=True)
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font on title?")
    text = blocks.RichTextBlock(
        blank=True,
        required=False,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
    )
    overlay = blocks.BooleanBlock(default=False, required=False, blank=True, help_text="Overlay text on image")
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Block text alignment")
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    image_alignment = RadioSelectBlock(
        choices=ImageAlignment.choices,
        default="left",
        help_text="Image left - text right, or image right - text left.",
    )
    orientation = blocks.ChoiceBlock(choices=Orientations.choices, default=Orientations.LANDSCAPE, help_text="Image orientation")
    size = blocks.ChoiceBlock(choices=ImageSizes.choices, default=ImageSizes.MEDIUM, help_text="Image size")
    crop = blocks.ChoiceBlock(choices=CropPercentage.choices, default=CropPercentage.FULL, help_text="Crop percentage")
    rounded = blocks.ChoiceBlock(choices=ImageRounding.choices, default=ImageRounding.NONE, help_text="Image rounding")
    responsive = blocks.BooleanBlock(required=False, default=False, help_text="Image responsive")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    link = LinkBlock()

    class Meta:
        template = "blocks/image_and_text_block.html"
        icon = "image"
        label = "Image & Text"
        label_format = "Image & Text {title}"


class LargeImageBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock(blank=True, null=True)
    orientation = blocks.ChoiceBlock(choices=Orientations.choices, default=Orientations.LANDSCAPE, help_text="Image orientation")
    size = blocks.ChoiceBlock(choices=ImageSizes.choices, default=ImageSizes.FULL_WIDTH, help_text="Image size")
    crop = blocks.ChoiceBlock(choices=CropPercentage.choices, default=CropPercentage.FULL, help_text="Crop percentage")
    rounded = blocks.ChoiceBlock(choices=ImageRounding.choices, default=ImageRounding.NONE, help_text="Image rounding")
    responsive = blocks.BooleanBlock(required=False, default=False, help_text="Image responsive")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    link = LinkBlock()

    class Meta:
        template = "blocks/large_image_block.html"
        icon = "image"
        label = "Large Image"
        label_format = "Large Image {image}"
