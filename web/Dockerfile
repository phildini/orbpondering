FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy entire repo (context must be repo root)
COPY pyproject.toml uv.lock* /app/
COPY src/ /app/src/
COPY web/ /app/web/

WORKDIR /app/web

# Install deps
RUN uv sync --no-dev

# Build Tailwind CSS
RUN npm install && npm run build

# Collect static files
RUN uv run python manage.py collectstatic --noinput

EXPOSE 8080
CMD ["uv", "run", "gunicorn", "orbpondering_web.wsgi", "--bind", "0.0.0.0:8080"]
