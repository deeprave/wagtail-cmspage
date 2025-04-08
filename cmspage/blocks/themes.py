# -*- coding: utf-8 -*-
#
# Metaclass for adding background and opacity fields to blocks

from django.db import models

__all__ = (
    "Backgrounds",
    "Palette",
    "Opacities",
    "Heights",
    "Insets",
    "SocialIcon",
    "Orientations",
    "Justifications",
    "ImageSizes",
    "IconColorChoices",
    "ImageAlignment",
    "CropPercentage",
)


# these intermediate classes explicitly define the metaclass `choices` property
# to avoid `noinspection PyUnresolvedReferences` warnings in PyCharm

class Choices(models.TextChoices):
    @property
    def choices(self):
        # noinspection PyUnresolvedReferences
        return super().choices


class IntChoices(models.IntegerChoices):
    @property
    def choices(self):
        # noinspection PyUnresolvedReferences
        return super().choices


class Backgrounds(Choices):
    NONE = "bg-transparent links-dark", "Transparent"
    PAGE = "bg-body links-dark", "Page"
    LIGHT = "bg-light links-dark", "Light"
    DARK = "bg-dark links-light", "Dark"
    WHITE = "bg-white links-dark", "White"
    BLACK = "bg-black links-light", "Black"
    PRIMARY = "bg-primary links-dark", "Primary"
    SECONDARY = "bg-secondary links-dark", "Secondary"
    TERTIARY = "bg-tertiary links-dark", "Tertiary"
    SUCCESS = "bg-success-subtle links-dark", "Success"
    WARNING = "bg-warning-subtle links-dark", "Warning"
    INFO = "bg-info-subtle links-dark", "Info"
    DANGER = "bg-danger-subtle links-dark", "Danger"


class Palette(Choices):
    NONE = f"{Backgrounds.NONE.value} text-dark title-dark", "Dark on Transparent"
    PAGE = f"{Backgrounds.PAGE.value} text-dark title-dark", "Dark on Page Background"
    LIGHT = f"{Backgrounds.LIGHT.value} text-dark title-dark", "Dark on Light Background"
    DARK = f"{Backgrounds.DARK.value} text-light title-light", "Light on Dark Background"
    WHITE = f"{Backgrounds.LIGHT.value} text-black title-dark", "Black on White Background"
    BLACK = f"{Backgrounds.WHITE.value} text-white title-light", "White on Black Background"
    PRIMARY = f"{Backgrounds.PRIMARY.value} text-dark title-dark", "Dark on Primary Background"
    SECONDARY = f"{Backgrounds.SECONDARY.value} text-dark title-dark", "Dark on Secondary Background"
    TERTIARY = f"{Backgrounds.TERTIARY.value} text-dark title-dark", "Dark on Tertiary Background"
    SUCCESS = f"{Backgrounds.SUCCESS.value} text-dark title-dark", "Dark on Success Background"
    WARNING = f"{Backgrounds.WARNING.value} text-dark title-dark", "Dark on Warning Background"
    INFO = f"{Backgrounds.INFO.value} text-dark title-dark", "Dark on Info Background"
    DANGER = f"{Backgrounds.DANGER.value} text-dark title-dark", "Dark on Danger Background"


class Opacities(Choices):
    OPACITY_FULL = "bg-opacity-100", "100%"
    OPACITY_75 = "bg-opacity-75", "75%"
    OPACITY_50 = "bg-opacity-50", "50%"
    OPACITY_25 = "bg-opacity-25", "25%"
    OPACITY_10 = "bg-opacity-10", "10%"


class Heights(Choices):
    SMALLEST = "height-0", "None"
    SMALL = "height-1 py-1", "Small"
    MEDIUM = "height-2 py-2", "Medium"
    LARGE = "height-3 py-3", "Large"
    LARGER = "height-4 py-4", "Larger"
    LARGEST = "height-5 py-5", "Largest"


class Insets(Choices):
    SMALLEST = "p-0", "None"
    SMALL = "p-1", "Small"
    MEDIUM = "p-2", "Medium"
    LARGE = "p-3", "Large"
    LARGER = "p-4", "Larger"
    LARGEST = "p-5", "Largest"


class SocialIcon(Choices):
    DISCORD = "discord", "Discord"
    EMAIL = "envelope", "Email"
    FACEBOOK = "facebook", "Facebook"
    GITHUB = "github", "GitHub"
    INSTAGRAM = "instagram", "Instagram"
    LINKEDIN = "linkedin", "LinkedIn"
    MEDIUM = "medium", "Medium"
    MESSENGER = "facebook-messenger", "Messenger"
    PINTEREST = "pinterest", "Pinterest"
    REDDIT = "reddit", "Reddit"
    RSS = "rss", "RSS"
    SKYPE = "skype", "Skype"
    SLACK = "slack", "Slack"
    SNAPCHAT = "snapchat", "Snapchat"
    TELEGRAM = "telegram", "Telegram"
    TIKTOK = "tiktok", "TikTok"
    TUMBLR = "tumblr", "Tumblr"
    TWITCH = "twitch", "Twitch"
    TWITTER = "twitter", "Twitter"
    VIMEO = "vimeo", "Vimeo"
    WHATSAPP = "whatsapp", "WhatsApp"
    X = "X", "X"
    YOUTUBE = "youtube", "YouTube"
    ZOOM = "zoom", "Zoom"


class IconColorChoices(Choices):
    BODY = "text-body", "Normal"
    WHITE = "text-white", "White"
    BLACK = "text-black", "Dark"
    PRIMARY = "text-primary", "Primary"
    SECONDARY = "text-secondary", "Secondary"
    TERTIARY = "text-tertiary", "Tertiary"
    SUCCESS = "text-success", "Success"
    WARNING = "text-warning", "Warning"
    INFO = "text-info", "Info"
    DANGER = "text-danger", "Danger"
    LIGHT = "text-light", "Light"
    DARK = "text-dark", "Dark"
    MUTED = "text-muted", "Muted"
    BLACK50 = "text-black-50", "Black 50% opacity"
    WHITE50 = "text-white-50", "White 50% opacity"


class Justifications(Choices):
    LEFT = "text-start", "Left"
    CENTER = "text-center", "Center"
    RIGHT = "text-end", "Right"


class Orientations(Choices):
    LANDSCAPE = "landscape", "Landscape"
    PORTRAIT = "portrait", "Portrait"
    SQUARE = "square", "Square"
    EXTRAWIDE = "extrawide", "Extra Wide"


class ImageSizes(Choices):
    TINY = "tiny", "Tiny"
    SMALL = "small", "Small"
    MEDIUM = "medium", "Medium"
    LARGE = "large", "Large"
    FULL_WIDTH = "full_width", "Full Width"
    ORIGINAL = "original", "Original"


class ImageAlignment(Choices):
    LEFT = "left", "Left"
    RIGHT = "right", "Right"
    CENTER = "center", "Center"
    FULL = "full", "Full"


class CropPercentage(IntChoices):
    NONE = 0, "None"
    SMALL = 25, "Small"
    MEDIUM = 50, "Medium"
    LARGE = 75, "Large"
    FULL = 100, "Full"


class ImageRounding(IntChoices):
    NONE = -1, "None"
    TINY = 0, "0"
    SMALL = 1, "1"
    MEDIUM = 2, "2"
    LARGE = 3, "3"
    LARGER = 4, "4"
    LARGEST = 5, "5"
