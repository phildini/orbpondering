.PHONY: install build-css dev

install:
	uv sync
	npm install

build-css:
	npm run build

dev-css:
	npm run watch

dev-server:
	uv run python manage.py runserver 0.0.0.0:8000

dev:
	@echo "Run in two terminals:"
	@echo "  make dev-css      — Tailwind CSS watch mode"
	@echo "  make dev-server   — Django dev server"
	@echo ""
	@echo "Or for a single command: open two terminals."
	@echo ""
	@echo "First time setup: make install && make build-css"
