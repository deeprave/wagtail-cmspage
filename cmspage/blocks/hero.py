from wagtail import blocks
from wagtail.images import blocks as image_blocks

from .background import BackgroundBlock
from .themes import Insets, Orientations, ImageSizes, CropPercentage, ImageRounding


class HeroImageBlock(blocks.StructBlock):
    image = image_blocks.ImageChooserBlock()
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    orientation = blocks.ChoiceBlock(choices=Orientations.choices, default=Orientations.LANDSCAPE, help_text="Image orientation")
    size = blocks.ChoiceBlock(choices=ImageSizes.choices, default=ImageSizes.MEDIUM, help_text="Image size")
    crop = blocks.ChoiceBlock(choices=CropPercentage.choices, default=CropPercentage.FULL, help_text="Crop percentage")
    rounded = blocks.ChoiceBlock(choices=ImageRounding.choices, default=ImageRounding.NONE, help_text="Image rounding")
    responsive = blocks.BooleanBlock(required=False, default=False, help_text="Image responsive")

    class Meta:
        template = "blocks/hero_block.html"
