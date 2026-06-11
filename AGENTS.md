# Orbpondering — Agent Guide

## Repository structure

This is a multi-package monorepo. Each package has its own `pyproject.toml`, `.venv`, and `uv.lock`.

```
src/orbpondering/    → Core Python library (tarot + astrology engine)
web/                 → Django web app (production on Fly.io)
client/              → BeeWare/Toga mobile client scaffold
```

## Commands

### Core library (run from repo root)

```bash
uv sync --all-extras           # install deps + dev + extras
uv run pytest tests/           # 119 tests, all passing
ruff check src/orbpondering/   # lint the core library
mypy src/orbpondering/         # type check
```

### Web app (run from `web/`)

```bash
uv sync --extra dev            # install deps + pytest
uv run devserver               # django runserver
uv run build-css               # rebuild Tailwind + DaisyUI
uv run pytest tests/           # 25 Django tests
ruff check .                   # lint the web app
npm install                    # first-time Tailwind setup
```

Or from repo root via `Makefile`:
```bash
make web-install               # uv sync + npm install + build-css
make web-dev                   # start Django devserver
```

### Docker / deploy

```bash
fly deploy                     # deploy web app to Fly.io (context = repo root)
```

**Build context is repo root**, not `web/`. Dockerfile at `web/Dockerfile`. The `.dockerignore` at repo root excludes `.venv`, `node_modules`, etc.

## Testing quirks

- **Core tests**: run from repo root with `uv run pytest tests/`. Test the orbpondering library (tarot draw, astrology, seed, models, houses, aspects).
- **Web tests**: run from `web/` with `uv run pytest tests/`. Test the accounts app (25 tests: models, signals, views, subscription gating). Uses pytest-django.
- CI only tests the core library on Python 3.12 (`.github/workflows/ci.yml`). The `feat/python-version-support` branch has an updated CI config that tests 3.10–3.14.

## Architecture notes

- **Core library**: `draw.py` is the main entrypoint (`tarot_draw_for_date`, `daily_tarot_draw`, `birth_tarot_draw`). Seeds are deterministic SHA-256 hashes of planetary positions.
- **Web app**: Django 6.0 + DRF. Has its own `pyproject.toml`. Depends on `orbpondering` via `[tool.uv.sources]` path reference (`{ path = "../" }`).
- **Auth**: `django-stagedoor` for email-magic-link login. `STAGEDOOR_DISABLE_USER_CREATION = False`. Login form at `/auth/token/`.
- **Payments**: Stripe via `accounts/stripe_integration.py`. Falls back to mock toggle when `STRIPE_SECRET_KEY` is not set. Webhook at `POST /accounts/stripe-webhook/`.
- **Styling**: Tailwind CSS + DaisyUI synthwave theme + custom `cyberpunk.css` (glass morphism, CRT grid, neon glows).
- **Infrastructure**: Fly.io with persistent volume at `/data` (SQLite DB + ephemeris cache). `docker-entrypoint.sh` runs migrations and sets site domain on startup.

## Gotchas

- `.dockerignore` at repo root — not in `web/`. Docker build context is the repo root.
- `fly.toml` is at repo root, references `web/Dockerfile`.
- Lint commands differ: `ruff check src/orbpondering/` (core) vs `ruff check web/` (web app).
- `ruff check web/` will fail if run from repo root without appropriate venv — use `source .venv/bin/activate` at root, then run ruff from either location.
- The root pyproject.toml has `requires-python = ">=3.12"` — libraries depend on astropy/numpy which don't support older Python.
- `feat/accounts-subscriptions` branch has the full accounts/subscriptions feature (user profiles, reading history, dashboard, Orb plan). Not yet merged to main.
