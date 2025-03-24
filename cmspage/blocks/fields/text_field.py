from wagtail.blocks import StructBlock, CharBlock, BooleanBlock


class TextFieldBlock(StructBlock):
    """A standard text field with label and input"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    default_value = CharBlock(required=False)

    class Meta:
        icon = "pilcrow"
        label = "Text Field"
        template = "blocks/form_fields/text_field_block.html"
