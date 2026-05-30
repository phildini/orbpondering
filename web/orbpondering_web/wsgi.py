"""WSGI application for production serving."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orbpondering_web.settings")

application = get_wsgi_application()
