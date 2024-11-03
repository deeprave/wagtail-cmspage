from wagtail import blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .background import BackgroundBlock
from .themes import Insets

class TitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    text = blocks.CharBlock(help_text="Title text to display")

    class Meta:
        template = "blocks/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"


class RichTextWithTitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=120,
        help_text="Display title, optional (max len=120)",
    )
    content = blocks.RichTextBlock(features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Rich text block, required")

    class Meta:
        template = "blocks/simple_richtext_block.html"
        label = "RichText with Title"
        icon = "doc-empty-inverse"
