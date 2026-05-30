"""API URL routing."""

from django.urls import path

from . import views

urlpatterns = [
    path("reading/", views.create_reading, name="api-create-reading"),
    path("reading/natal/", views.create_natal_reading, name="api-create-natal-reading"),
]
