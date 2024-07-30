# -*- coding: utf-8 -*-
import re

from django import template
from django.template import TemplateSyntaxError
from django.template.base import token_kwargs
from django.template.loader_tags import IncludeNode, construct_relative_path

register = template.Library()


@register.filter(name="embedurl")
def get_embed_url_with_parameters(url):
    if any(youtube in url for youtube in ("youtube.com", "youtu.be")):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)"  # Get video id from URL
        embed_url = re.sub(regex, r"https://www.youtube.com/embed/\1", url)  # Append video id to desired URL
        print(embed_url)
        return f"{embed_url}?rel=0"
    return url


@register.tag("smart_include")
def smart_include(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError(
            "%r tag takes at least one argument: the name of the template to "
            "be included." % bits[0]
        )
    options = {}
    remaining_bits = bits[2:]
    while remaining_bits:
        option = remaining_bits.pop(0)
        if option in options:
            raise TemplateSyntaxError(
                "The %r option was specified more than once." % option
            )
        if option == "with":
            value = token_kwargs(remaining_bits, parser, support_legacy=False)
            if not value:
                raise TemplateSyntaxError(
                    '"with" in %r tag needs at least one keyword argument.' % bits[0]
                )
        elif option == "only":
            value = True
        else:
            raise TemplateSyntaxError(
                "Unknown argument for %r tag: %r." % (bits[0], option)
            )
        options[option] = value
    isolated_context = options.get("only", False)
    namemap = options.get("with", {})
    bits[1] = construct_relative_path(parser.origin.template_name, bits[1])
    included = parser.compile_filter(bits[1])
    return IncludeNode(
        included,
        extra_context=namemap,
        isolated_context=isolated_context,
    )

    # try:
    #     return do_include(parser, token)
    # except (TemplateDoesNotExist, TemplateSyntaxError):
    #     return TextNode("")
