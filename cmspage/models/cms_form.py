from wagtail.fields import StreamField

from .cms_page import CMSPageBase
from cmspage.blocks import FormBlock


class CMSFormPage(CMSPageBase):
    """
    A specialized CMS page type designed for building forms.
    """
    page_description = "This page type is for building forms"
    # parent_page_types = ["cmspage.CMSHomePage", "cmspage.CMSPage"]
    # subpage_types = []

    # Extend body_blocks like CMSHomePage but without the hero block
    body_blocks = [
        ("form", FormBlock()),
    ] + CMSPageBase.body_blocks
    body = StreamField(body_blocks, blank=True, null=True)

    class Meta:
        app_label = "cmspage"
        verbose_name = "CMS Form Page"
        verbose_name_plural = "CMS Form Pages"
