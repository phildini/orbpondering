"""Main entry point for Orbpondering."""

import argparse
import sys
from pathlib import Path

from orbpondering.cli import main as cli_main
from orbpondering.display import display_reading


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="orbpondering",
        description="Tarot spreads seeded by daily astrological calculations",
    )

    # Add TUI flag
    parser.add_argument(
        "--tui", action="store_true", help="Launch the Textual TUI interface"
    )

    # Add reversed flag from Phase 0
    parser.add_argument(
        "--reversed",
        "-r",
        action="store_true",
        help="Show cards as reversed (30-50% of cards)",
    )

    # Add config flag for Phase 0
    parser.add_argument(
        "--config",
        type=str,
        help="Path to config file (default: ~/.config/orbpondering/config.toml)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Handle TUI mode
    if args.tui:
        # Launch TUI
        from orbpondering.tui import TUIApp

        app = TUIApp()
        app.run()
        return

    # Handle CLI mode
    cli_main(args)


if __name__ == "__main__":
    main()
