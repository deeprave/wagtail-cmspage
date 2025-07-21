# -*- coding: utf-8 -*-
#
# Metaclass for adding background and opacity fields to blocks

from django.db import models

__all__ = (
    "Palette",
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



class Palette(Choices):
    # New semantic palette using cp-* classes
    NONE = "cp-transparent", "Transparent Background"
    PAGE = "cp-page", "Page Theme (respects light/dark mode)"
    LIGHT = "cp-light", "Light Theme (fixed light)"
    DARK = "cp-dark", "Dark Theme (fixed dark)"
    WHITE = "cp-white", "Black on White"
    BLACK = "cp-black", "White on Black"
    HIGHLIGHT = "cp-highlight", "Highlight Theme (alternate background)"
    STANDOUT = "cp-standout", "Standout Theme (secondary alternate)"
    SUCCESS = "cp-success", "Success (green for positive actions)"
    WARNING = "cp-warning", "Warning (yellow for caution)"
    INFO = "cp-info", "Info (using site palette colors)"
    DANGER = "cp-danger", "Danger (red for errors/critical)"


class Heights(Choices):
    SMALLEST = "height-0", "None"
    SMALL = "height-1 py-1", "Small"
    MEDIUM = "height-2 py-2", "Medium"
    LARGE = "height-3 py-3", "Large"
    LARGER = "height-4 py-4", "Larger"
    LARGEST = "height-5 py-5", "Largest"


class Insets(Choices):
    SMALLEST = "p-0", "None"
    SMALL = "p-1 p-sm-2", "Small (responsive)"
    MEDIUM = "p-2 p-sm-3", "Medium (responsive)"
    LARGE = "p-3 p-sm-4", "Large (responsive)"
    LARGER = "p-4 p-sm-5", "Larger (responsive)"
    LARGEST = "p-5 p-sm-6", "Largest (responsive)"


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
