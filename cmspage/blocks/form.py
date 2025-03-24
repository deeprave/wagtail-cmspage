from wagtail.blocks import StructBlock, CharBlock, TextBlock, StreamBlock

from cmspage.blocks.fields import (
    TextFieldBlock,
    TextAreaFieldBlock,
    EmailFieldBlock,
    IntegerFieldBlock,
    DecimalFieldBlock,
    SelectFieldBlock,
    MultiSelectFieldBlock,
)


class FormBlock(StructBlock):
    """Top level form container"""
    form_title = CharBlock(required=True, help_text="Form title displayed at the top")
    form_description = TextBlock(required=False, help_text="Description of the form's purpose")
    submit_url = CharBlock(required=True, help_text="URL to which the form data is to be submitted")
    submit_button_text = CharBlock(default="Submit", required=True)
    success_message = CharBlock(default="Form submitted successfully", required=True)

    fields = StreamBlock([
        ("text_field", TextFieldBlock()),
        ("textarea_field", TextAreaFieldBlock()),
        ("email_field", EmailFieldBlock()),
        ("integer_field", IntegerFieldBlock()),
        ("decimal_field", DecimalFieldBlock()),
        ("select_field", SelectFieldBlock()),
        ("multiselect_field", MultiSelectFieldBlock()),
    ])

    class Meta:
        icon = "form"
        label = "Form"
        template = "blocks/form_block.html"
