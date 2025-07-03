"""
Minimal URL configuration for tests
"""
from django.urls import path, include
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("cms-admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]
