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
)

class Choices(models.TextChoices):
    @property
    def choices(self):
        # noinspection PyUnresolvedReferences
        return super().choices

class Backgrounds(Choices):
    NONE = "bg-transparent", "Transparent"
    PAGE = "bg-body", "Page"
    LIGHT = "bg-light", "Light"
    DARK = "bg-dark", "Dark"
    WHITE = "bg-white", "White"
    BLACK = "bg-black", "Black"
    PRIMARY = "bg-primary", "Primary"
    SECONDARY = "bg-secondary", "Secondary"
    SUCCESS = "bg-success", "Success"
    WARNING = "bg-warning", "Warning"
    INFO = "bg-info", "Info"
    DANGER = "bg-danger", "Danger"


class Palette(Choices):
    NONE = "bg-transparent text-dark title-dark links-dark", "Dark on Transparent"
    PAGE = "bg-body text-dark title-dark links-dark", "Dark on Page Background"
    LIGHT = "bg-light text-dark title-dark links-dark", "Dark on Light Background"
    DARK = "bg-dark text-light title-light links-light", "Light on Dark Background"
    WHITE = "bg-white text-black title-dark links-dark", "Black on White Background"
    BLACK = "bg-black text-white title-light links-light", "White on Black Background"
    PRIMARY = "bg-primary text-dark title-dark links-dark", "Dark on Primary Background"
    SECONDARY = "bg-secondary text-dark title-dark links-dark", "Dark on Secondary Background"
    TERTIARY = "bg-tertiary text-dark title-dark links-dark", "Dark on Tertiary Background"
    SUCCESS = "bg-success-subtle text-dark title-dark links-dark", "Dark on Success Background"
    WARNING = "bg-warning-subtle text-dark title-dark links-dark", "Dark on Warning Background"
    INFO = "bg-info-subtle text-dark title-dark links-dark", "Dark on Info Background"
    DANGER = "bg-danger-subtle text-dark title-dark links-dark", "Dark on Danger Background"


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
    LEFT = "text-left", "Left"
    CENTER = "text-center", "Center"
    RIGHT = "text-right", "Right"
