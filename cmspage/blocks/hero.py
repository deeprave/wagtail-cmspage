from wagtail import blocks
from wagtail.images import blocks as image_blocks

from .background import BackgroundBlock
from .themes import Insets


class HeroImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    image = image_blocks.ImageChooserBlock()

    class Meta:
        template = "blocks/hero_block.html"
