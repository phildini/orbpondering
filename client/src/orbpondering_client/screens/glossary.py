"""Planet, element, and modality glossary screen."""

import toga
from toga.sources.list_source import ListSource
from toga.style import Pack
from toga.style.pack import COLUMN

PLANET_DATA = [
    ("☉", "Sun", "Core identity, ego, life force, vitality. Represents your fundamental self."),
    ("☽", "Moon", "Emotions, intuition, subconscious, habits. Governs your inner world."),
    ("☿", "Mercury", "Communication, thinking, travel, intellect. Rules the mind."),
    ("♀", "Venus", "Love, beauty, values, relationships, money. Governs attraction."),
    ("♂", "Mars", "Action, drive, desire, ambition, aggression. Rules energy and initiative."),
    ("♃", "Jupiter", "Expansion, luck, wisdom, growth, optimism. Brings abundance."),
    ("♄", "Saturn", "Structure, discipline, responsibility, lessons, time. Brings limitations and maturity."),
    ("♅", "Uranus", "Change, innovation, rebellion, breakthroughs, freedom. Rules the unexpected."),
    ("♆", "Neptune", "Dreams, illusion, spirituality, intuition, confusion. Rules transcendence."),
    ("♇", "Pluto", "Transformation, power, rebirth, depth, the unconscious. Rules endings and regeneration."),
]

MODALITY_DATA = [
    ("🔥", "Cardinal", "Initiating, leadership, beginnings. Starts new seasons: Aries, Cancer, Libra, Capricorn."),
    ("💠", "Fixed", "Stabilizing, persistence, resistance. Sustains the season: Taurus, Leo, Scorpio, Aquarius."),
    ("🌊", "Mutable", "Adapting, flexibility, change. Transitions between seasons: Gemini, Virgo, Sagittarius, Pisces."),
]

ELEMENT_DATA = [
    ("🔥", "Fire", "Action, energy, passion, inspiration. Signs: Aries, Leo, Sagittarius."),
    ("💧", "Water", "Emotion, intuition, depth, sensitivity. Signs: Cancer, Scorpio, Pisces."),
    ("💨", "Air", "Thought, communication, ideas, connection. Signs: Gemini, Libra, Aquarius."),
    ("🌍", "Earth", "Practicality, stability, matter, sensuality. Signs: Taurus, Virgo, Capricorn."),
]


class GlossaryScreen(toga.Box):
    """Reference screen explaining planets, elements, and modalities."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN))
        self._app = app

        scroll = toga.ScrollContainer(style=Pack(flex=1))
        content = toga.Box(style=Pack(direction=COLUMN, padding=20))

        # Planets section
        content.add(
            toga.Label(
                "Planets",
                style=Pack(font_weight="bold", font_size=16, padding=(0, 0, 8, 0)),
            )
        )
        planets_rows = [
            {"icon": None, "title": f"{s} {n}", "subtitle": d}
            for s, n, d in PLANET_DATA
        ]
        content.add(
            toga.DetailedList(
                data=ListSource(planets_rows),
                style=Pack(padding=(0, 0, 20, 0)),
            )
        )

        # Modalities section
        content.add(
            toga.Label(
                "Modalities (Qualities)",
                style=Pack(font_weight="bold", font_size=16, padding=(0, 0, 8, 0)),
            )
        )
        mod_rows = [
            {"icon": None, "title": n, "subtitle": d}
            for _, n, d in MODALITY_DATA
        ]
        content.add(
            toga.DetailedList(
                data=ListSource(mod_rows),
                style=Pack(padding=(0, 0, 20, 0)),
            )
        )

        # Elements section
        content.add(
            toga.Label(
                "Elements",
                style=Pack(font_weight="bold", font_size=16, padding=(0, 0, 8, 0)),
            )
        )
        elem_rows = [
            {"icon": None, "title": f"{s} {n}", "subtitle": d}
            for s, n, d in ELEMENT_DATA
        ]
        content.add(
            toga.DetailedList(
                data=ListSource(elem_rows),
                style=Pack(padding=(0, 0, 12, 0)),
            )
        )

        # Back button
        content.add(
            toga.Button(
                "Back",
                on_press=lambda w: self._back(),
                style=Pack(padding=(8, 0, 0, 0)),
            )
        )

        scroll.content = content
        self.add(scroll)

    def _back(self) -> None:
        reading = self._app.reading
        if reading and reading.get("chart"):
            self._app.open_chart()
        else:
            self._app.open_reading(reading)
