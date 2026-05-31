#!/bin/bash
set -e

# Ensure runtime directories exist (volume mount at /data)
mkdir -p /data/cache

if [ -n "$DJANGO_DB_PATH" ]; then
    mkdir -p "$(dirname "$DJANGO_DB_PATH")"
fi

# Run database migrations
uv run python manage.py migrate --noinput

# Start gunicorn
exec uv run gunicorn orbpondering_web.wsgi --bind 0.0.0.0:8080
