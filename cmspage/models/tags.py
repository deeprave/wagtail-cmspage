from django.db import models
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase, Tag as TaggitTag
from wagtail.snippets.models import register_snippet


class PageTag(TaggedItemBase):
    content_object = ParentalKey("wagtailcore.Page", on_delete=models.CASCADE, related_name="cmspage_tags")


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True
