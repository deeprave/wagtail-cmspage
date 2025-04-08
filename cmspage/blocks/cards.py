from wagtail import blocks
from wagtail.images import blocks as image_blocks

from .background import BackgroundBlock
from .links import LinkBlock
from .themes import Palette, Insets, Justifications, Orientations, ImageSizes, CropPercentage, ImageRounding
from .. import DEFAULT_RICHTEXTBLOCK_FEATURES


class Card(blocks.StructBlock):
    title = blocks.CharBlock(
        blank=True,
        null=True,
        required=False,
        max_length=255,
        label="Card Title",
        help_text="Bold title text for this card (len=255)",
    )
    text = blocks.RichTextBlock(
        required=False,
        blank=True,
        null=True,
        features=DEFAULT_RICHTEXTBLOCK_FEATURES,
        label="Card Text",
        help_text="Optional text for this card",
    )
    justify = blocks.ChoiceBlock(
        required=False, choices=Justifications.choices, default=Justifications.LEFT, help_text="Text alignment"
    )
    image = image_blocks.ImageChooserBlock(required=False, blank=True, null=True, label="Card Image")
    orientation = blocks.ChoiceBlock(choices=Orientations.choices, default=Orientations.LANDSCAPE, help_text="Image orientation")
    size = blocks.ChoiceBlock(choices=ImageSizes.choices, default=ImageSizes.MEDIUM, help_text="Image size")
    crop = blocks.ChoiceBlock(choices=CropPercentage.choices, default=CropPercentage.FULL, help_text="Crop percentage")
    responsive = blocks.BooleanBlock(required=False, default=False, help_text="Image responsive")
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Cards palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    link = LinkBlock(required=False, label="Card Link", help_text="Enter a page or document, or an external link")

    class Meta:
        icon = "page"
        label = "Card"
        label_format = "Card {title}"


class CardsBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    cursive = blocks.BooleanBlock(required=False, default=False, help_text="Use the cursive font in titles?")
    rounded = blocks.ChoiceBlock(required=False, choices=ImageRounding.choices, default=ImageRounding.NONE, help_text="Image rounding")
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
        label_format = "Cards Block"
