# -*- coding: utf-8 -*-
import re
from django.template import Template, Context
from django import template
from wagtail.images.models import Image

register = template.Library()


@register.filter(name="embedurl")
def get_embed_url_with_parameters(url):
    if any(youtube in url for youtube in ("youtube.com", "youtu.be")):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"  # Get video id from URL
        embed_url = re.sub(regex, r"https://www.youtube.com/embed/\1", url)  # Append video id to desired URL
        print(embed_url)
        return f"{embed_url}?rel=0"
    return url


RAW_SIZES = {  # landscape (width, height),
    # portrait (width, height),
    # square (width, height),
    # extrawide (width, height)
    "tiny": ((150, 100), (100, 150), (150, 150), (450, 150)),
    "small": ((300, 200), (200, 300), (300, 300), (900, 300)),
    "medium": ((480, 320), (320, 480), (480, 480), (1440, 480)),
    "large": ((600, 400), (400, 600), (600, 600), (1800, 600)),
    "full_width": ((800, 533), (533, 800), (800, 800), (2400, 800)),
    "original": ((None, None), (None, None), (None, None), (None, None)),
}

ORIENTATIONS = ["landscape", "portrait", "square", "extrawide"]

IMAGE_SIZES = {}
for orientation_index, orientation in enumerate(ORIENTATIONS):
    IMAGE_SIZES[orientation] = {}
    for size, size_tuple in RAW_SIZES.items():
        dims = size_tuple[orientation_index]
        IMAGE_SIZES[orientation][size] = "original" if dims[0] is None else f"{dims[0]}x{dims[1]}"


@register.simple_tag
def render_image(
    image: Image,
    orientation: str = "landscape",
    size: str = "medium",
    size_prefix: str = "fill",
    alt_text: str = None,
    crop: str | int = None,
    rounded: int = None,
    responsive: bool = True,
):
    """
    Creates and renders a template for the specified image rendition.
    """
    # Get the spec or default to medium landscape
    css_classes = ["img-fluid"] if responsive else []
    if rounded:
        css_classes.append(f"rounded-{rounded}")
    css_class = f' class="{" ".join(css_classes)}"' if css_classes else ""

    dimensions = IMAGE_SIZES.get(orientation, {}).get(size)
    image_size = ("original" if dimensions == "original" else f"{size_prefix}-{dimensions}") if dimensions else size
    cropping = f"-c{crop}" if crop and dimensions != "original" else ""

    alt_text = alt_text or image.title or image.description or ""
    alt = f' alt="{alt_text}"' if alt_text else ""

    # Create a template string with the specific image tag
    template_string = f"""
    {{% load wagtailimages_tags %}}
    {{% image image {image_size}{cropping} format-webp as webp_image %}}
    <source srcset="{{{{ webp_image.url }}}}" type="image/webp"{css_class}>
    {{% image image {image_size} as the_image %}}
    <img src="{{ image.url }}" {alt}{css_class}>
    """

    # Create and render the template
    t = Template(template_string)
    context = Context({"image": image})
    return t.render(context)
