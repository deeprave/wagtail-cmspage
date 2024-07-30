#!/usr/bin/env python
from pathlib import Path
import random
import string

import django
from django.conf import settings

LETTERS = string.ascii_letters + string.digits
KEYLEN = 50

if not settings.configured:
    BASE_DIR = Path(__file__).resolve().parent
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

    # Configure test environment
    settings.configure(
        SECRET_KEY="".join(random.choice(LETTERS) for _ in range(KEYLEN)),
        DATABASES=DATABASES,
        INSTALLED_APPS=(
            "cmspage",
            "wagtail.contrib.forms",
            "wagtail.contrib.redirects",
            "wagtail.contrib.table_block",
            "wagtail.embeds",
            "wagtail.sites",
            "wagtail.users",
            "wagtail.snippets",
            "wagtail.documents",
            "wagtail.images",
            "wagtail.search",
            "wagtail.admin",
            "wagtail",
            "taggit",
            "modelcluster",
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "django.contrib.sites",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.admin.apps.SimpleAdminConfig",
            "django.contrib.staticfiles",
        ),
        ROOT_URLCONF="",  # tests override urlconf, but it still needs to be defined
        MIDDLEWARE_CLASSES=(
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
        ),
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [
                    BASE_DIR / "templates",
                ],
                "APP_DIRS": False,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.debug",
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                        "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ],
        FORMS_URLFIELD_ASSUME_HTTPS=True,
        WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS=False,
    )

django.setup()
