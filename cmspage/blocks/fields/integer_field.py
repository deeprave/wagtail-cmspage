from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, IntegerBlock


class IntegerFieldBlock(StructBlock):
    """An integer field"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    default_value = IntegerBlock(required=False)
    min_value = IntegerBlock(required=False)
    max_value = IntegerBlock(required=False)

    class Meta:
        icon = "order"
        label = "Integer Field"
        template = "blocks/form_fields/integer_field_block.html"
