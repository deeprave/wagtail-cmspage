from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, DecimalBlock, IntegerBlock


class DecimalFieldBlock(StructBlock):
    """A decimal field with precision"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    default_value = DecimalBlock(required=False)
    min_value = DecimalBlock(required=False)
    max_value = DecimalBlock(required=False)
    decimal_places = IntegerBlock(default=2, required=False)

    class Meta:
        icon = "plus"
        label = "Decimal Field"
        template = "blocks/form_fields/decimal_field_block.html"
