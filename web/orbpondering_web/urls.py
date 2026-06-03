"""Root URL configuration."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("orbpondering_web.api.urls")),
    path("auth/", include("stagedoor.urls", namespace="stagedoor")),
    path("", include("orbpondering_web.frontend.urls")),
]
