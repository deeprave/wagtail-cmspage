from wagtail import blocks

from cmspage import DEFAULT_RICHTEXTBLOCK_FEATURES
from .links import LinkBlock
from .themes import Insets, Palette, Justifications


class CallToActionBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=60,
        help_text="Max length of 60 characters, optional",
    )
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font?")
    text = blocks.RichTextBlock(
        required=False,
        blank=True,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        help_text="Call to action text, optional (max=200)",
    )
    justify = blocks.ChoiceBlock(required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="CTA palette",
        label="CTA Button palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    link = LinkBlock(required=False, blank=True, null=True)

    class Meta:
        template = "blocks/call_to_action_block.html"
        icon = "warning"
        label = "Call to Action"
        label_format = "Call to Action {title}"
