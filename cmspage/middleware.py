# middleware.py

from django.conf import settings


class ConditionalDebugToolbarMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def enable(self, request):
        return False if request.GET.get("in_preview_panel", False) else settings.DEBUG

    def __call__(self, request):
        settings.DEBUG_TOOLBAR_CONFIG["SHOW_TOOLBAR_CALLBACK"] = self.enable(request)

        return self.get_response(request)
