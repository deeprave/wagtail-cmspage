# -*- coding: utf-8 -*-
import re

from django import template
register = template.Library()


@register.filter(name="embedurl")
def get_embed_url_with_parameters(url):
    if any(youtube in url for youtube in ("youtube.com", "youtu.be")):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"  # Get video id from URL
        embed_url = re.sub(regex, r"https://www.youtube.com/embed/\1", url)  # Append video id to desired URL
        print(embed_url)
        return f"{embed_url}?rel=0"
    return url
