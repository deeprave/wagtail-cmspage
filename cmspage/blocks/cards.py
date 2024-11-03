from wagtail import blocks
from wagtail.images import blocks as image_blocks

from .background import BackgroundBlock
from .links import LinkBlock
from .themes import Palette, Insets


class Card(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Cards palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=255,
        label="Card Title",
        help_text="Bold title text for this card (len=255)",
    )
    text = blocks.RichTextBlock(
        blank=True, null=True, required=False, label="Card Text", help_text="Optional text for this card"
    )
    image = image_blocks.ImageChooserBlock(required=False, label="Card Image", help_text="Image (resized)")
    link = LinkBlock(required=False, label="Card Link", help_text="Enter a page or document, or an external link")


class CardsBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    cards = blocks.ListBlock(Card())

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        numcards = len(value["cards"])
        context.update(
            {
                "numcards": numcards,
                "colspread": 12 if numcards < 2 else 6 if numcards == 2 else 4 if numcards == 3 else 3,
            }
        )
        return context

    class Meta:
        template = "blocks/cards_block.html"
        icon = "image"
        label = "Set of Cards"
