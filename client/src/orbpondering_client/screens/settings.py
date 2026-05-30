"""Settings screen with input form."""

from datetime import date

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class SettingsScreen(toga.Box):
    """Form for entering astrological parameters."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN, padding=20))
        self._app = app

        self.date_input = toga.TextInput(
            value=date.today().isoformat(),
            placeholder="YYYY-MM-DD",
            style=Pack(padding=(0, 0, 10, 0)),
        )
        self.lat_input = toga.TextInput(
            value="0.0", placeholder="Latitude", style=Pack(flex=1, padding=(0, 5, 10, 0))
        )
        self.lon_input = toga.TextInput(
            value="0.0", placeholder="Longitude", style=Pack(flex=1, padding=(0, 0, 10, 0))
        )

        self.house_select = toga.Selection(
            items=["whole_sign", "equal", "porphyry", "placidus"],
            style=Pack(padding=(0, 0, 10, 0)),
        )
        self.spread_select = toga.Selection(
            items=["daily", "three_card", "celtic_cross"],
            style=Pack(padding=(0, 0, 10, 0)),
        )

        self.calculate_btn = toga.Button(
            "Calculate Reading",
            on_press=self.calculate,
            style=Pack(padding=(10, 0, 0, 0)),
        )
        self.status = toga.Label("", style=Pack(padding=(10, 0, 0, 0)))

        self.add(
            toga.Label("Date", style=Pack(padding=(0, 0, 2, 0))),
            self.date_input,
            toga.Box(
                children=[
                    toga.Label("Lat", style=Pack(width=30, padding=(0, 0, 10, 0))),
                    self.lat_input,
                    toga.Label("Lon", style=Pack(width=30, padding=(0, 0, 10, 0))),
                    self.lon_input,
                ],
                style=Pack(direction=ROW),
            ),
            toga.Label("House System", style=Pack(padding=(0, 0, 2, 0))),
            self.house_select,
            toga.Label("Spread", style=Pack(padding=(0, 0, 2, 0))),
            self.spread_select,
            self.calculate_btn,
            self.status,
        )

    async def calculate(self, widget):
        """Fetch reading from API and show results."""
        self.status.text = "Calculating..."
        self.calculate_btn.enabled = False

        try:
            from ..api import create_reading

            reading = create_reading(
                date=self.date_input.value,
                lat=float(self.lat_input.value or "0.0"),
                lon=float(self.lon_input.value or "0.0"),
                house_system=self.house_select.value,
                spread=self.spread_select.value,
            )

            from .results import ResultsScreen
            self._app.main_window.content = ResultsScreen(self._app, reading)
        except Exception as e:
            self.status.text = f"Error: {e}"
            self.calculate_btn.enabled = True
