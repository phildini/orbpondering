"""Test configuration for Django web app tests."""

import os

import django


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orbpondering_web.settings")
    django.setup()
