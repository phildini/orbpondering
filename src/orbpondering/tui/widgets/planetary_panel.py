"""Planetary panel widget for the TUI."""

from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from orbpondering.models import Chart


class PlanetaryPanel(Container):
    """Widget to display planetary positions in the TUI."""

    DEFAULT_CSS = """
    PlanetaryPanel {
        border: solid $primary;
        background: $surface;
        padding: 1 2;
        width: 30;
    }

    PlanetaryPanel .planetary-row {
        layout: horizontal;
        height: 3;
    }

    PlanetaryPanel .planetary-name {
        width: 15;
        color: $text;
    }

    PlanetaryPanel .planetary-position {
        width: 15;
        color: $secondary;
    }

    PlanetaryPanel .planetary-symbol {
        width: 5;
        color: $accent;
        text-align: center;
    }
    """

    def __init__(self, chart: Chart | None = None, **kwargs: Any) -> None:
        """Initialize the planetary panel."""
        super().__init__(**kwargs)
        self.chart = chart

    def compose(self) -> ComposeResult:
        """Compose the planetary panel."""
        if self.chart is None:
            yield Static("No chart data available")
            return

        for body, position in self.chart.planetary_positions.items():
            row = Container(classes="planetary-row")

            symbol = self._get_planet_symbol(body)
            name_text = f"{symbol} {body.title()}"

            longitude = position.longitude
            degree = longitude % 30
            sign_symbol = position.zodiac_sign.symbol

            position_text = f"{degree:.0f}° {sign_symbol}"

            row.mount(Static(name_text, classes="planetary-name"))
            row.mount(Static(position_text, classes="planetary-position"))
            row.mount(Static(sign_symbol, classes="planetary-symbol"))

            yield row

    def update_chart(self, chart: Chart) -> None:
        """Update the chart displayed in this panel."""
        self.chart = chart

        for child in list(self.children):
            child.remove()

        if chart is None:
            self.mount(Static("No chart data available"))
            return

        for body, position in chart.planetary_positions.items():
            row = Container(classes="planetary-row")
            self.mount(row)

            symbol = self._get_planet_symbol(body)
            name_text = f"{symbol} {body.title()}"

            longitude = position.longitude
            degree = longitude % 30
            sign_symbol = position.zodiac_sign.symbol

            position_text = f"{degree:.0f}° {sign_symbol}"

            row.mount(Static(name_text, classes="planetary-name"))
            row.mount(Static(position_text, classes="planetary-position"))
            row.mount(Static(sign_symbol, classes="planetary-symbol"))

    def _get_planet_symbol(self, planet_name: str) -> str:
        """Get the unicode symbol for a planet."""
        symbols = {
            "sun": "☉",
            "moon": "☽",
            "mercury": "☿",
            "venus": "♀",
            "mars": "♂",
            "jupiter": "♃",
            "saturn": "♄",
            "uranus": "♅",
            "neptune": "♆",
            "pluto": "♇",
        }
        return symbols.get(planet_name.lower(), "?")
