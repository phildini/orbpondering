"""Root URL configuration."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("orbpondering_web.api.urls")),
    path("", include("orbpondering_web.frontend.urls")),
]
