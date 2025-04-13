from wagtail import blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .themes import Palette, Insets

class LineItemBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, help_text="Line text (max len=120)")
    content = blocks.RichTextBlock(required=False, features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Dropdown text block, optional")

    class Meta:
        template = "blocks/lineitem_block.html"
        icon = "arrow-down"
        label = "Line Content"


class AbstractLinesBlock(blocks.StructBlock):
    subtitle = blocks.CharBlock(required=False, help_text="Lines Title (optional)")
    number = blocks.BooleanBlock(required=False, default=False, help_text="Add number to lines")
    dropdown = blocks.BooleanBlock(required=False, default=False, help_text="Dropdown text (accordian)")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="LineBlock palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

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
