# -*- coding: utf-8 -*-
#
# Metaclass for adding background and opacity fields to blocks

from django.db import models
from wagtail import blocks


class Backgrounds(models.TextChoices):
    NONE = "bg-transparent", "Transparent"
    PAGE = "bg-body", "Page"
    LIGHT = "bg-light", "Light"
    DARK = "bg-dark", "Dark"
    WHITE = "bg-white", "White"
    BLACK = "bg-black", "Dark"
    PRIMARY = "bg-primary", "Primary"
    SECONDARY = "bg-secondary", "Secondary"
    SUCCESS = "bg-success", "Success"
    WARNING = "bg-warning", "Warning"
    INFO = "bg-info", "Info"
    DANGER = "bg-danger", "Danger"


class Opacities(models.TextChoices):
    OPACITY_FULL = "bg-opacity-100", "100%"
    OPACITY_75 = "bg-opacity-75", "75%"
    OPACITY_50 = "bg-opacity-50", "50%"
    OPACITY_25 = "bg-opacity-25", "25%"
    GRADIENT = "bg-gradient", "Gradient"


class BlockBackgroundMeta(blocks.DeclarativeSubBlocksMetaclass):
    def __new__(cls, name, bases, attrs):
        attrs["background"] = blocks.ChoiceBlock(
            choices=Backgrounds.choices,
            default=Backgrounds.NONE,
            help_text="Background type or color",
        )
        attrs["opacity"] = blocks.ChoiceBlock(
            choices=Opacities.choices,
            default=Opacities.OPACITY_FULL,
            help_text="Background opacity",
        )
        return super().__new__(cls, name, bases, attrs)
