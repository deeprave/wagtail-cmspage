from wagtail import blocks

from .background import BackgroundBlock
from .themes import Heights


class NewSectionBlock(blocks.StructBlock):
    height = blocks.ChoiceBlock(
        choices=Heights.choices, default=Heights.MEDIUM, help_text="Vertical space height"
    )
    bg = BackgroundBlock()

    class Meta:
        template = "blocks/new_section.html"
        icon = "collapse-down"
        label = "Vertical space"
        label_format = "Vertical space {height}"
