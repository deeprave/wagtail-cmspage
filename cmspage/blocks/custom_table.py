from wagtail import blocks
from wagtail.contrib.table_block import blocks as table_blocks

from .background import BackgroundBlock
from .themes import Insets


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
