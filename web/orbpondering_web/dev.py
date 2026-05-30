"""Dev workflow helpers — invoked via `uv run <command>` from web/."""

import subprocess
import sys


def _run(cmd: list[str]) -> None:
    sys.exit(subprocess.run(cmd).returncode)


def build_css() -> None:
    """Build Tailwind CSS for production."""
    _run(["npm", "run", "build"])


def watch_css() -> None:
    """Watch Tailwind CSS for changes (dev mode)."""
    _run(["npm", "run", "watch"])


def dev() -> None:
    """Install dependencies and start dev server."""
    _run(["npm", "install"])
    devserver()


def devserver() -> None:
    """Run the Django dev server."""
    _run(["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"])


def collectstatic() -> None:
    """Collect Django static files."""
    _run(["uv", "run", "python", "manage.py", "collectstatic", "--noinput"])
