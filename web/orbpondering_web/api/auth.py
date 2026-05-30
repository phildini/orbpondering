"""API key authentication middleware."""

import os

from django.conf import settings
from django.http import HttpRequest, JsonResponse


class APIKeyMiddleware:
    """Validates X-API-Key header on /api/ endpoints."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path.startswith("/api/"):
            expected = os.environ.get("ORBPONDERING_API_KEY") or getattr(
                settings, "ORBPONDERING_API_KEY", ""
            )
            provided = request.META.get("HTTP_X_API_KEY", "")
            if not provided or provided != expected:
                return JsonResponse({"error": "Unauthorized"}, status=401)
        return self.get_response(request)
