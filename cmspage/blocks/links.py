from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from wagtail import blocks
from wagtail.documents import blocks as document_blocks

from .themes import Palette, Insets


class LinkValue(blocks.StructValue):
    """
    Generates a URL and Title for blocks with multiple link choices.
    """

    @property
    def link_title(self):
        if not (title := self.get("title")):
            if not (title := self.get("button_title")):
                if not (title := self.get("page_link")):
                    if not (title := self.get("doc_link")):
                        title = self.get("extra_link").title
        return title

    @property
    def link_url(self):
        page_url = self.get("page_link").url if self.get("page_link") else None
        doc_url = self.get("doc_link").url if self.get("doc_link") else None
        extra_link = self.get("extra_link")
        if page_url and extra_link:
            return f"{page_url}{extra_link}"
        return page_url or doc_url or extra_link


ONE_LINK_ERROR_MESSAGE = "You must select a page or document, or enter an external link."
INVALID_LINK_ERROR_MESSAGE = "Invalid link. Please select a page or document, or enter a valid URL."


class LinkBlock(blocks.StructBlock):
    button_title = blocks.CharBlock(
        required=False,
        max_length=255,
        label="Button Title (use hyphen for special link button)",
    )
    page_link = blocks.PageChooserBlock(
        required=False,
        label="Page link",
    )
    doc_link = document_blocks.DocumentChooserBlock(
        required=False,
        label="Document link",
    )
    extra_link = blocks.CharBlock(
        required=False,
        max_length=255,
        label="Extra link",
    )

    def clean(self, value):
        errors = {}
        page_link = value.get("page_link")
        doc_link = value.get("doc_link")
        extra_link = value.get("extra_link")
        if sum((bool(page_link), bool(doc_link), bool(extra_link))) > 1:
            errors["page_link"] = ErrorList([ONE_LINK_ERROR_MESSAGE])
            errors["doc_link"] = ErrorList(["ONE_LINK_ERROR_MESSAGE"])
            errors["extra_link"] = ErrorList([ONE_LINK_ERROR_MESSAGE])

        if errors:
            raise ValidationError(INVALID_LINK_ERROR_MESSAGE, params=errors)
        return super().clean(value)

    class Meta:
        value_class = LinkValue


class LinksBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="Cards palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    title = blocks.CharBlock(
        required=False,
        blank=True,
        null=True,
        max_length=255,
        label="links Title",
        help_text="Bold title text for this set of links (len=255)",
    )
    links = blocks.ListBlock(LinkBlock())

    class Meta:
        template = "blocks/links_block.html"
        icon = "link"
        label = "Set of Links"
