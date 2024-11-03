from wagtail import blocks
from wagtail.blocks import ListBlock
from wagtail.images.blocks import ImageChooserBlock

from .background import BackgroundBlock
from .themes import Insets


class CarouselImageStructBlock(blocks.StructBlock):
    """
    A class that represents an image in a carousel.

    Attributes:
        RICHTEXTBLOCK_FEATURES (list): A list of rich text block features.
        carousel_image (ForeignKey): A foreign key to each image.
        carousel_title (CharField): The display title of the image.
        carousel_content (RichTextField): Rich text content.
        carousel_attribution (CharField): Attribution of the image.

    Methods:
        None

    """

    RICHTEXTBLOCK_FEATURES = ["bold", "italic", "ol", "ul", "usefont"]

    # noinspection PyUnresolvedReferences
    carousel_image = ImageChooserBlock()
    carousel_title = blocks.CharBlock(required=False, max_length=120, help_text="Display title, optional (max len=120)")
    carousel_content = blocks.RichTextBlock(required=False, features=RICHTEXTBLOCK_FEATURES, max_length=256, help_text="Short description")
    carousel_attribution = blocks.CharBlock(required=False, max_length=80, help_text="Attribution, optional (max len=80)")


class CarouselImageBlock(blocks.StructBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    carousel_interval = blocks.IntegerBlock(default=12000, help_text="Keep visible for time in milliseconds",)
    carousel = ListBlock(CarouselImageStructBlock())

    class Meta:
        template = "blocks/carousel_block.html"
        icon = "image"
        label = "Carousel"
