from wagtail import blocks

from .themes import Palette, Insets


class CopyrightBlock(blocks.StructBlock):
    copyright = blocks.CharBlock(help_text="Copyright notice to display in the footer")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Section palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

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
