from django import forms
from wagtail import blocks

from .background import BackgroundBlock
from .themes import Insets

class RadioSelectBlock(blocks.ChoiceBlock):
    bg = BackgroundBlock()
    inset = blocks.ChoiceBlock(
        choices=Insets.choices, default=Insets.SMALL, help_text="Padding around the block"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field.widget = forms.RadioSelect(choices=self.field.widget.choices)
