from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, TextBlock, IntegerBlock


class TextAreaFieldBlock(StructBlock):
    """A multi-line text input with label"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    default_value = TextBlock(required=False)
    rows = IntegerBlock(default=3, required=False)

    class Meta:
        icon = "doc-full"
        label = "Text Area Field"
        template = "blocks/form_fields/textarea_field_block.html"
