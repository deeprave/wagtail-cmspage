import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from wagtail.rich_text import LinkHandler
from wagtail.snippets.models import register_snippet

from .views import MenuLinkViewSet

register_snippet(MenuLinkViewSet)


class UsefontClassHandler(LinkHandler):
    identifier = "usefont"

    @staticmethod
    def expand_db_attributes(attrs):
        return f"<span class=\"usefont\">{attrs.get('href')}</span>"


def register_custom_class_feature(features):
    feature_name = "usefont"
    type_ = "USEFONT"
    tag = "usefont"

    control = {
        "type": type_,
        "label": "𝕱",
        "description": "Use special font",
        "style": {"backgroundColor": "lightcyan"},
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag} }
    }
    features.register_converter_rule("content_state", feature_name, db_conversion)
    features.default_features.append(feature_name)

hooks.register("register_rich_text_features", register_custom_class_feature)
