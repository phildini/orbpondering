"""Main screen implementation for the TUI."""

import asyncio
from datetime import date
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Label, Static

from ..widgets.planetary_panel import PlanetaryPanel
from ..widgets.spread_layout import SpreadLayout


class MainScreen(Screen):
    """Main dashboard screen."""

    CSS_PATH = "main.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "open_settings", "Settings"),
        ("y", "show_help", "Help"),
        ("f5", "save_reading", "Save Reading"),
        ("h", "show_history", "History"),
        ("c", "calculate", "Calculate"),
    ]

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the main screen."""
        super().__init__(**kwargs)
        self.current_view = "spread"
        self.show_reversed = False
        self.last_lat = 0.0
        self.last_lon = 0.0
        self.last_spread = "daily"
        self._is_calculating = False

    def compose(self) -> ComposeResult:
        """Compose the main screen layout."""
        yield Label("[b]ORBPONDERING[/b]", id="dashboard-title")
        yield Static("", id="status-message")
        yield Horizontal(
            Vertical(
                Label("[b]Settings[/b]", id="settings-header"),
                Label("Date: Today", id="setting-date-label"),
                Label("Lat: 0.0", id="setting-lat-label"),
                Label("Lon: 0.0", id="setting-lon-label"),
                Label("House: whole_sign", id="setting-house-label"),
                Label("Spread: daily", id="setting-spread-label"),
                Container(
                    Button(
                        "Calculate",
                        id="calculate-btn",
                        variant="primary",
                        disabled=False,
                    ),
                    Button("Settings", id="settings-btn"),
                    id="main-controls",
                ),
                id="settings-panel",
            ),
            Vertical(
                Label("[b]Spread View[/b]", id="spread-view-title"),
                SpreadLayout(id="spread-layout"),
                id="spread-view-panel",
            ),
            Vertical(
                Label("[b]Chart Details[/b]", id="chart-panel-title"),
                PlanetaryPanel(id="planetary-panel"),
                id="chart-panel",
            ),
            id="main-content",
        )

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self._update_widgets()

    def on_screen_resumed(self) -> None:
        """Called when this screen is resumed."""
        pending_update = getattr(self.app, "_pending_reading_update", False)
        if pending_update:
            setattr(self.app, "_pending_reading_update", False)
        self._update_widgets()

    def _update_widgets(self) -> None:
        """Update widgets with current reading."""
        app = self.app
        reading = getattr(app, "reading", None)

        status_msg = self.query_one("#status-message", Static)
        if reading is None:
            status_msg.update("Press 'Calculate' to draw a reading")
            return

        status_msg.update(
            f"Reading: {reading.spread.name} | Seed: {str(reading.seed)[:8]}..."
        )

        try:
            if reading.chart:
                panel = self.query_one("#planetary-panel", PlanetaryPanel)
                panel.update_chart(reading.chart)
        except Exception:
            pass

        try:
            if reading.positions:
                spread = self.query_one("#spread-layout", SpreadLayout)
                spread.populate(list(reading.positions))
        except Exception:
            pass

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_show_help(self) -> None:
        """Show help information."""
        self.notify(
            "F1: Help | F2: Settings | F5: Save | H: History | C: Calculate | Q: Quit"
        )

    def action_open_settings(self) -> None:
        """Open the settings screen."""
        from .settings import SettingsScreen

        self.app.push_screen(SettingsScreen())

    def action_calculate(self) -> None:
        """Calculate a reading with current or default settings."""
        if self._is_calculating:
            self.notify("Calculation already in progress...")
            return

        self._start_calculation()

    def _start_calculation(self) -> None:
        """Start the async calculation."""
        self._is_calculating = True
        self.query_one("#calculate-btn", Button).disabled = True
        status_msg = self.query_one("#status-message", Static)
        status_msg.update("[b]Calculating...[/b] (first use may take a few seconds)")
        self.refresh()

        loop = asyncio.get_event_loop()
        loop.create_task(self._run_calculation())

    async def _run_calculation(self) -> None:
        """Run the calculation in background and update UI when done."""
        from orbpondering.constants import HouseSystem
        from orbpondering.draw import tarot_draw_for_date

        def do_calculation() -> Any:
            return tarot_draw_for_date(
                d=date.today(),
                lat=self.last_lat,
                lon=self.last_lon,
                house_system=HouseSystem.WHOLE_SIGN,
                spread_name=self.last_spread,
                reversed_cards=self.show_reversed,
            )

        reading = await asyncio.get_event_loop().run_in_executor(None, do_calculation)

        setattr(self.app, "reading", reading)

        self._is_calculating = False

        await self._update_after_calculation(reading)

    async def _update_after_calculation(self, reading: Any) -> None:
        """Update UI after calculation completes."""
        status_msg = self.query_one("#status-message", Static)
        status_msg.update(
            f"Reading: {reading.spread.name} | Seed: {str(reading.seed)[:8]}..."
        )

        try:
            if reading.chart:
                panel = self.query_one("#planetary-panel", PlanetaryPanel)
                panel.update_chart(reading.chart)
        except Exception:
            pass

        try:
            if reading.positions:
                spread = self.query_one("#spread-layout", SpreadLayout)
                spread.populate(list(reading.positions))
        except Exception:
            pass

        self.query_one("#calculate-btn", Button).disabled = False
        self.notify(
            f"Drew {len(reading.positions)} cards: {reading.positions[0].card.name}"
        )

    def action_save_reading(self) -> None:
        """Save the current reading."""
        reading = getattr(self.app, "reading", None)
        if reading is None:
            self.notify("No reading to save. Calculate a reading first.")
            return

        from orbpondering.service import save_reading

        try:
            save_reading(reading)
            self.notify("Reading saved successfully!")
        except Exception as e:
            self.notify(f"Failed to save reading: {e}")

    def action_show_history(self) -> None:
        """Show the reading history screen."""
        from .history import ReadingHistoryScreen

        self.app.push_screen(ReadingHistoryScreen())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "calculate-btn":
            self.action_calculate()
        elif event.button.id == "settings-btn":
            self.action_open_settings()

    def show_card_detail(self, card_position: Any, index: int, total: int) -> None:
        """Show card detail modal."""
        from .card_detail import CardDetailView

        self.app.push_screen(CardDetailView(card_position, index, total))
