from wagtail import blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .themes import Insets, Justifications, Palette


class TitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(help_text="Title text to display")
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font on title?")
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.CENTER, help_text="Title text alignment")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    class Meta:
        template = "blocks/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centered text to display on the page"


class RichTextWithTitleBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=120,
        help_text="Display title, optional (max len=120)",
    )
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font on title?")
    content = blocks.RichTextBlock(features=DEFAULT_RICHTEXTBLOCK_FEATURES, help_text="Rich text block, required")
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    class Meta:
        template = "blocks/simple_richtext_block.html"
        label = "RichText with Title"
        icon = "doc-empty-inverse"
