"""Root URL configuration."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("orbpondering_web.api.urls")),
    path("auth/", include("stagedoor.urls", namespace="stagedoor")),
    path("accounts/", include("orbpondering_web.accounts.urls")),
    path("", include("orbpondering_web.frontend.urls")),
]
