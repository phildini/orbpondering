"""Status bar widget for the TUI."""

from datetime import datetime
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static


class StatusBar(Static):
    """Bottom status bar showing key bindings and current state."""

    DEFAULT_CSS = """
    StatusBar {
        height: 3;
        background: $boost;
        color: $text-muted;
    }

    StatusBar .status-section {
        width: auto;
        padding: 0 2;
    }

    StatusBar .status-key {
        color: $accent;
    }

    StatusBar .status-value {
        color: $text;
    }
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the status bar."""
        super().__init__(**kwargs)
        self.current_mode = "Transit"
        self.seed_hash = "N/A"
        self.show_reversed = False

    def compose(self) -> ComposeResult:
        """Compose the status bar."""
        yield Horizontal(
            Static("Mode: ", classes="status-section"),
            Static(self.current_mode, classes="status-value mode-display"),
            Static(" | ", classes="status-section"),
            Static("Seed: ", classes="status-section"),
            Static(self.seed_hash[:8] if self.seed_hash != "N/A" else "N/A", classes="status-value seed-display"),
            Static(" | ", classes="status-section"),
            Static("Reversed: ", classes="status-section"),
            Static("On" if self.show_reversed else "Off", classes="status-value reversed-display"),
            Static(" | ", classes="status-section"),
            Static(datetime.now().strftime("%Y-%m-%d %H:%M"), classes="status-value timestamp"),
            id="status-bar-content",
        )

    def set_mode(self, mode: str) -> None:
        """Set the current mode display."""
        self.current_mode = mode
        self._update_mode_display()

    def set_seed(self, seed: int) -> None:
        """Set the seed hash display."""
        self.seed_hash = str(seed)
        self._update_seed_display()

    def set_reversed(self, enabled: bool) -> None:
        """Set the reversed mode display."""
        self.show_reversed = enabled
        self._update_reversed_display()

    def _update_mode_display(self) -> None:
        """Update the mode display widget."""
        try:
            mode_widget = self.query_one(".mode-display", Static)
            mode_widget.update(self.current_mode)
        except Exception:
            pass

    def _update_seed_display(self) -> None:
        """Update the seed display widget."""
        try:
            seed_value = self.seed_hash[:8] if self.seed_hash != "N/A" else "N/A"
            seed_widget = self.query_one(".seed-display", Static)
            seed_widget.update(seed_value)
        except Exception:
            pass

    def _update_reversed_display(self) -> None:
        """Update the reversed mode display widget."""
        try:
            reversed_widget = self.query_one(".reversed-display", Static)
            reversed_widget.update("On" if self.show_reversed else "Off")
        except Exception:
            pass

    def refresh_timestamp(self) -> None:
        """Refresh the timestamp display."""
        try:
            timestamp_widget = self.query_one(".timestamp", Static)
            timestamp_widget.update(datetime.now().strftime("%Y-%m-%d %H:%M"))
        except Exception:
            pass
