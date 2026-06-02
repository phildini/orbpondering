"""Reading results screen displaying tarot cards."""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

ELEMENT_COLORS = {
    "fire": "#e74c3c",
    "water": "#3498db",
    "air": "#f39c12",
    "earth": "#27ae60",
}


def _element_color(element: str | None) -> str:
    return ELEMENT_COLORS.get(element, "#6c5ce7")


class ReadingScreen(toga.Box):
    """Display completed tarot reading with card details."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN))
        self._app = app
        reading = app.reading
        if reading is None:
            return

        scroll = toga.ScrollContainer(style=Pack(flex=1))
        content = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # Header
        spread_name = reading.get("spread", {}).get("name", "Reading")
        seed = reading.get("seed", 0)
        content.add(
            toga.Label(
                spread_name,
                style=Pack(font_weight="bold", font_size=18, padding=(0, 0, 2, 0)),
            )
        )
        content.add(
            toga.Label(
                f"Seed: {seed}  —  The SHA-256 hash of today's planetary positions.",
                style=Pack(font_size=10, padding=(0, 0, 16, 0)),
            )
        )

        # Cards
        positions = reading.get("positions", [])
        for pos in positions:
            card = pos.get("card", {})
            element = card.get("element")
            color = _element_color(element)

            card_box = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=(6, 8),
                    background_color=color,
                )
            )
            inner = toga.Box(
                style=Pack(
                    direction=COLUMN,
                    padding=12,
                    background_color="#1a1a2e",
                )
            )

            # Card name + orientation
            name_row = toga.Box(style=Pack(direction=ROW))
            upright = card.get("upright", True)
            arrow = "↑" if upright else "↓"
            name_row.add(
                toga.Label(
                    f"{card.get('name', '?')}",
                    style=Pack(flex=1, font_weight="bold", font_size=14),
                )
            )
            name_row.add(
                toga.Label(arrow, style=Pack(font_size=16, color=color))
            )
            inner.add(name_row)

            # Position label
            inner.add(
                toga.Label(
                    pos.get("label", ""),
                    style=Pack(font_size=11, padding=(2, 0, 6, 0)),
                )
            )

            # Arcana / suit
            arcana = card.get("arcana", "").title()
            suit = card.get("suit", "")
            if suit:
                arcana_suit = f"{arcana} · {suit}"
            else:
                arcana_suit = f"{arcana} Arcana"
            inner.add(
                toga.Label(arcana_suit, style=Pack(font_size=11, padding=(0, 0, 4, 0)))
            )

            # Keywords
            keywords = card.get("keywords", [])
            if keywords:
                inner.add(
                    toga.Label(
                        ", ".join(keywords),
                        style=Pack(font_size=10, padding=(0, 0, 4, 0)),
                    )
                )

            # House number
            house = pos.get("house_number")
            if house is not None:
                inner.add(
                    toga.Label(
                        f"House {house}",
                        style=Pack(font_size=10, padding=(0, 0, 0, 0)),
                    )
                )

            card_box.add(inner)
            content.add(card_box)

        # Buttons
        if reading.get("chart"):
            content.add(
                toga.Button(
                    "View Planetary Chart",
                    on_press=lambda w: app.open_chart(),
                    style=Pack(padding=(16, 0, 4, 0)),
                )
            )

        content.add(
            toga.Button(
                "Planet Glossary",
                on_press=lambda w: app.open_glossary(),
                style=Pack(padding=(4, 0, 4, 0)),
            )
        )

        content.add(
            toga.Button(
                "New Reading",
                on_press=lambda w: app.back_to_settings(),
                style=Pack(padding=(12, 0, 0, 0)),
            )
        )

        scroll.content = content
        self.add(scroll)
