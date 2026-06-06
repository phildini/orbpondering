#!/bin/bash
set -e

# Ensure runtime directories exist (volume mount at /data)
mkdir -p /data/cache

if [ -n "$DJANGO_DB_PATH" ]; then
    mkdir -p "$(dirname "$DJANGO_DB_PATH")"
fi

# Run database migrations
uv run python manage.py migrate --noinput

# Update site domain from env (defaults to fly.dev)
if [ -n "$SITE_DOMAIN" ]; then
    uv run python manage.py shell -c "
from django.contrib.sites.models import Site
Site.objects.filter(id=1).update(domain='$SITE_DOMAIN', name='Orbpondering')
" 2>/dev/null || true
fi

# Start gunicorn with access logs to stdout
exec uv run gunicorn orbpondering_web.wsgi \
    --bind 0.0.0.0:8080 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
