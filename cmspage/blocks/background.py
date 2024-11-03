from wagtail import blocks

from .themes import Backgrounds, Opacities


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
