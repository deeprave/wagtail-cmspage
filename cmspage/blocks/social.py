from django import forms
from django.utils.functional import cached_property
from wagtail.telepath import register
from wagtail import blocks
# noinspection PyProtectedMember
from wagtail.blocks.struct_block import StructBlockAdapter

from .themes import SocialIcon, Palette, Insets

URI_PATTERN = (
    r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:/{0,3}[a-zA-Z0-9.-]+(?:/?|[/?]\S*)"
    r"|mailto:[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
)


class SocialLinkBlock(blocks.StructBlock):
    icon = blocks.ChoiceBlock(
        choices=SocialIcon.choices, default=SocialIcon.EMAIL, help_text="Social media icon"
    )
    name = blocks.CharBlock(max_length=120, help_text="Social media name")
    url = blocks.RegexBlock(URI_PATTERN, help_text="Social media URL")

    class Meta:
        template = "blocks/social_link_block.html"
        icon = "link"
        label = "Social Link"


class SocialLinkBlockAdapter(StructBlockAdapter):
    js_constructor = "cmspage.blocks.SocialLinkBlock"

    @cached_property
    def media(self):
        structblock_media = super().media
        # noinspection PyProtectedMember
        return forms.Media(
            js=structblock_media._js + ["js/social-link-block.js"],
            css=structblock_media._css,
        )


class SocialsBlock(blocks.StructBlock):
    palette = blocks.ChoiceBlock(
        choices=Palette.choices, default=Palette.WARNING, help_text="LineBlock palette"
    )
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )
    links = blocks.ListBlock(SocialLinkBlock())

    class Meta:
        template = "blocks/socials_block.html"
        icon = "site"
        label = "Social Links"

register(SocialLinkBlockAdapter(), SocialLinkBlock)
