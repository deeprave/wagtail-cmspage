from wagtail.blocks import StructBlock, CharBlock, BooleanBlock, EmailBlock


class EmailFieldBlock(StructBlock):
    """An email field with validation"""
    label = CharBlock(required=True, help_text="The label for this field")
    help_text = CharBlock(required=False, help_text="Optional help text for this field")
    required = BooleanBlock(required=False, help_text="Is this field required?")
    default_value = EmailBlock(required=False)

    class Meta:
        icon = "mail"
        label = "Email Field"
        template = "blocks/form_fields/email_field_block.html"
