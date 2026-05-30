"""Frontend URL routing."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reading/", views.reading_view, name="reading-form"),
]
