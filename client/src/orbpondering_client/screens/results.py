"""Results screen displaying a tarot reading."""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN


class ResultsScreen(toga.Box):
    """Display a completed tarot reading."""

    def __init__(self, app, reading):
        super().__init__(style=Pack(direction=COLUMN, padding=20))
        self._app = app

        spread_name = reading.get("spread", {}).get("name", "Reading")
        seed = reading.get("seed", 0)

        cards_box = toga.Box(style=Pack(direction=COLUMN, padding=(10, 0)))
        for pos in reading.get("positions", []):
            card = pos.get("card", {})
            card_box = toga.Box(style=Pack(direction=COLUMN, padding=5))
            card_box.add(
                toga.Label(
                    f"{card.get('name', '?')} — {pos.get('label', '')}",
                    style=Pack(font_weight="bold"),
                )
            )
            card_box.add(
                toga.Label(
                    f"{card.get('arcana', '').title()} · {'↑ Upright' if card.get('upright', True) else '↓ Reversed'}"
                )
            )
            keywords = card.get("keywords", [])
            if keywords:
                card_box.add(toga.Label(", ".join(keywords)))
            cards_box.add(card_box)

        scroll = toga.ScrollContainer(style=Pack(flex=1))
        scroll.content = cards_box

        self.add(
            toga.Label(spread_name, style=Pack(font_weight="bold", font_size=16)),
            toga.Label(f"Seed: {seed}", style=Pack(padding=(0, 0, 10, 0))),
            scroll,
            toga.Button(
                "New Reading",
                on_press=self.new_reading,
                style=Pack(padding=(10, 0, 0, 0)),
            ),
        )

    def new_reading(self, widget):
        """Go back to settings screen."""
        from .settings import SettingsScreen

        self._app.main_window.content = SettingsScreen(self._app)
