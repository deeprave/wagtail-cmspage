from wagtail.blocks import StructBlock, CharBlock, ListBlock, BooleanBlock


class OptionBlock(StructBlock):
    """An option for select fields"""
    label = CharBlock(required=True, help_text="Display text for this option")
    value = CharBlock(required=True, help_text="Value when this option is selected")


class SelectFieldBlock(StructBlock):
    """A dropdown select field"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    options = ListBlock(OptionBlock())
    default_value = CharBlock(required=False, help_text="Value must match one of the options")

    class Meta:
        icon = "arrow-down"
        label = "Select Field"
        template = "blocks/form_fields/select_field_block.html"


class MultiSelectFieldBlock(StructBlock):
    """A multi-select field"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    options = ListBlock(OptionBlock())

    class Meta:
        icon = "list-ul"
        label = "Multi-Select Field"
        template = "blocks/form_fields/multi_select_field_block.html"
