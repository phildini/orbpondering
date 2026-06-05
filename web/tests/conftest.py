"""Test configuration for Django web app tests."""

import django
import os


def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orbpondering_web.settings")
    django.setup()
