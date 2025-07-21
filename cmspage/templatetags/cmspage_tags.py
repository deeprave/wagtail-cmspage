# -*- coding: utf-8 -*-
import re
from django.template import Template, Context, TemplateSyntaxError
from django import template
from django.template.loader import get_template
from wagtail.images.models import Image

register = template.Library()


class SafeIncludeNode(template.Node):
    """
    A Node that safely includes templates, handling cases where the template variable is empty or None.
    Only suppresses errors related to missing/empty template variables, not actual template errors.
    """
    def __init__(self, template_expr):
        self.template_expr = template_expr

    def render(self, context):
        try:
            template_name = self.template_expr.resolve(context)
        except template.VariableDoesNotExist:
            # If variable doesn't exist, return empty string silently
            return ""

        # If template name is empty, None, or evaluates to False, return empty string
        if not template_name:
            return ""

        # Get the template - let TemplateDoesNotExist and other template errors bubble up
        template_obj = get_template(template_name)

        # Convert context to dict for template rendering
        include_context = context.flatten()

        # Render the included template - let all template errors bubble up
        return template_obj.render(include_context)


@register.tag("cmspage_include")
def cmspage_include(parser, token):
    """
    Template tag that safely includes templates, gracefully handling empty template variables.

    Usage:
        {% load cmspage_tags %}
        {% cmspage_include template_variable %}

    If template_variable is None, empty, or doesn't exist, returns empty string instead of error.
    All other template errors (TemplateDoesNotExist, syntax errors, etc.) bubble up normally.
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise TemplateSyntaxError("'cmspage_include' tag requires exactly one argument")

    # Get the template expression
    template_expr = parser.compile_filter(bits[1])

    return SafeIncludeNode(template_expr)


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
