"""Accounts URL routing."""

from django.urls import path

from . import stripe_integration, views

urlpatterns = [
    path("dashboard/", views.dashboard, name="accounts-dashboard"),
    path("settings/", views.settings_view, name="accounts-settings"),
    path("profiles/", views.profiles_view, name="accounts-profiles"),
    path("pricing/", views.pricing_view, name="accounts-pricing"),
    path("subscribe/", views.subscribe_view, name="accounts-subscribe"),
    path("stripe-webhook/", stripe_integration.stripe_webhook, name="stripe-webhook"),
]
