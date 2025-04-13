from wagtail import blocks

from .themes import Heights, Palette, Insets


class NewSectionBlock(blocks.StructBlock):
    height = blocks.ChoiceBlock(
        choices=Heights.choices, default=Heights.MEDIUM, help_text="Vertical space height"
    )
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    class Meta:
        template = "blocks/new_section.html"
        icon = "collapse-down"
        label = "Vertical space"
        label_format = "Vertical space {height}"
