#!/usr/bin/env python
from pathlib import Path
import random
import string

from testcontainers.postgres import PostgresContainer

import django
from django.conf import settings

LETTERS = string.ascii_letters + string.digits
KEYLEN = 50

if not settings.configured:
    BASE_DIR = Path(__file__).resolve().parent
    POSTGRES_USER = "pguser"
    POSTGRES_PASSWORD = "pgpass"
    POSTGRES_DB = "pgdb"

    postgres_container = PostgresContainer(
        "postgres:16-alpine", username=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB, driver="psychopg"
    )
    postgres_container.start()

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": postgres_container.get_container_host_ip(),
            "PORT": postgres_container.get_exposed_port(5432),
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
        }
    }

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
        ROOT_URLCONF="tests.urls",  # Use minimal test URL configuration
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
        WAGTAILADMIN_STATIC_FILE_VERSION_STRINGS=False,
    )

django.setup()
