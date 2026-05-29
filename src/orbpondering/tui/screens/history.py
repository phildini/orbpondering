"""Reading history screen for the TUI."""

from datetime import date
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container, ScrollableContainer, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from orbpondering.service import get_readings_dir


class ReadingHistoryScreen(Screen):
    """Screen to view past tarot readings."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
    ]

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the reading history screen."""
        super().__init__(**kwargs)
        self.readings: list[tuple[date, int, str]] = []

    def compose(self) -> ComposeResult:
        """Compose the reading history screen."""
        yield Container(
            Label("READING HISTORY", id="history-title"),
            ScrollableContainer(
                Vertical(id="readings-list"),
                id="readings-scroll",
            ),
            Container(
                Button("Back", id="back-btn"),
                id="history-buttons",
            ),
            id="history-screen",
        )

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self._load_readings()

    def _load_readings(self) -> None:
        """Load readings from the readings directory."""
        readings_dir = get_readings_dir()
        if not readings_dir.exists():
            self._show_empty_state()
            return

        self.readings = []
        for file_path in readings_dir.glob("*.json"):
            try:
                parts = file_path.stem.split("_")
                if len(parts) >= 2:
                    reading_date = date.fromisoformat(parts[0])
                    seed = int(parts[1]) if parts[1].isdigit() else 0
                    spread_type = "Unknown"
                    self.readings.append((reading_date, seed, spread_type))
            except (ValueError, IndexError):
                continue

        self._display_readings()

    def _show_empty_state(self) -> None:
        """Show empty state when no readings are available."""
        readings_list = self.query_one("#readings-list", Vertical)
        for child in list(readings_list.children):
            child.remove()
        readings_list.mount(
            Static("No saved readings yet.", id="no-readings-message"),
        )

    def _display_readings(self) -> None:
        """Display the list of readings."""
        readings_list = self.query_one("#readings-list", Vertical)
        for child in list(readings_list.children):
            child.remove()

        if not self.readings:
            self._show_empty_state()
            return

        for reading_date, seed, spread_type in sorted(self.readings, reverse=True):
            reading_item = Container(
                Static(f"{reading_date.isoformat()}", classes="reading-date"),
                Static(f"Seed: {str(seed)[:8]}...", classes="reading-seed"),
                Static(f"Type: {spread_type}", classes="reading-type"),
                Button("Load", id=f"load-{seed}", classes="reading-load-btn"),
                id=f"reading-{seed}",
            )
            readings_list.mount(reading_item)

    def action_go_back(self) -> None:
        """Go back to the main screen."""
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "back-btn":
            self.action_go_back()
        elif event.button.id and event.button.id.startswith("load-"):
            seed_str = event.button.id.replace("load-", "")
            if seed_str.isdigit():
                self._load_reading(int(seed_str))

    def _load_reading(self, seed: int) -> None:
        """Load a specific reading by seed."""
        pass
