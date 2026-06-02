"""Planetary chart screen with DetailedList."""

import toga
from toga.sources.list_source import ListSource
from toga.style import Pack
from toga.style.pack import COLUMN

ELEMENT_COLORS = {
    "fire": "#e74c3c",
    "water": "#3498db",
    "air": "#f39c12",
    "earth": "#27ae60",
}

PLANET_SYMBOLS = {
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


class ChartScreen(toga.Box):
    """Display planetary positions and chart angles."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN))
        self._app = app
        chart = app.reading.get("chart") if app.reading else None
        if chart is None:
            self.add(toga.Label("No chart data available"))
            return

        scroll = toga.ScrollContainer(style=Pack(flex=1))
        content = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # Header
        content.add(
            toga.Label(
                "Planetary Positions",
                style=Pack(font_weight="bold", font_size=16, padding=(0, 0, 12, 0)),
            )
        )

        # DetailedList for planets
        rows = []
        planets = chart.get("planets", {})
        for name, p in planets.items():
            symbol = PLANET_SYMBOLS.get(name, "?")
            element_icon = {
                "fire": "🔥",
                "water": "💧",
                "air": "💨",
                "earth": "🌍",
            }.get(p.get("element", ""), "")

            title = f"{symbol} {name.title()} — {p.get('degree', 0):.0f}° {p.get('sign', '')}"
            subtitle = (
                f"{element_icon} {p.get('element', '').title()} · "
                f"{p.get('modality', '').title()}"
            )
            if p.get("meaning"):
                subtitle += f" — {p['meaning']}"

            rows.append({
                "icon": None,
                "title": title,
                "subtitle": subtitle,
            })

        planet_list = toga.DetailedList(
            data=ListSource(rows),
            style=Pack(flex=1, padding=(0, 0, 12, 0)),
        )
        content.add(planet_list)

        # Angles section
        asc = chart.get("ascendant", 0)
        mc = chart.get("midheaven", 0)
        dominant = chart.get("dominant_element", "")

        angles_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                padding=12,
                background_color="#1a1a2e",
            )
        )
        angles_box.add(
            toga.Label(
                f"Ascendant: {asc:.1f}°  —  The sign rising on the eastern horizon.",
                style=Pack(font_size=11, padding=(0, 0, 4, 0)),
            )
        )
        angles_box.add(
            toga.Label(
                f"MC (Midheaven): {mc:.1f}°  —  The highest point in the sky.",
                style=Pack(font_size=11, padding=(0, 0, 4, 0)),
            )
        )
        dom_color = ELEMENT_COLORS.get(dominant, "#fff")
        angles_box.add(
            toga.Label(
                f"Dominant Element: {dominant.title()}",
                style=Pack(
                    font_size=11,
                    font_weight="bold",
                    color=dom_color,
                ),
            )
        )
        content.add(angles_box)

        # Back button
        content.add(
            toga.Button(
                "Back to Reading",
                on_press=lambda w: app.open_reading(app.reading),
                style=Pack(padding=(16, 0, 0, 0)),
            )
        )
        content.add(
            toga.Button(
                "Planet Glossary",
                on_press=lambda w: app.open_glossary(),
                style=Pack(padding=(4, 0, 0, 0)),
            )
        )

        scroll.content = content
        self.add(scroll)
