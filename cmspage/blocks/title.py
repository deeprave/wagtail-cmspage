from wagtail import blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .background import BackgroundBlock
from .themes import Insets, Justifications


class TitleBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.CENTER, help_text="Text alignment")
    text = blocks.CharBlock(help_text="Title text to display")
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font?")

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
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font?")
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
    content = blocks.RichTextBlock(features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Rich text block, required")

    class Meta:
        template = "blocks/simple_richtext_block.html"
        label = "RichText with Title"
        icon = "doc-empty-inverse"
