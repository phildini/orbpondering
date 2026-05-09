"""Tests for data model construction, immutability, and relationships."""

from dataclasses import FrozenInstanceError, fields, is_dataclass
from datetime import date

import pytest

from orbpondering.cards import Card
from orbpondering.constants import Arcana, HouseSystem, Suit
from orbpondering.models import CardPosition, Chart, PlanetaryPosition, TarotReading
from orbpondering.spreads import Spread


class TestChartDataclass:
    def test_chart_is_dataclass(self) -> None:
        assert is_dataclass(Chart)

    def test_chart_creation(self, sample_date, sample_location) -> None:
        chart = Chart(
            date=sample_date,
            latitude=sample_location["lat"],
            longitude=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            planetary_positions={},
            ascendant=123.45,
            midheaven=234.56,
            house_cusps=[
                0.0,
                30.0,
                60.0,
                90.0,
                120.0,
                150.0,
                180.0,
                210.0,
                240.0,
                270.0,
                300.0,
                330.0,
            ],
            seed=987654321,
            dominant_element="fire",
        )
        assert chart.date == sample_date
        assert chart.latitude == pytest.approx(40.7128)
        assert chart.longitude == pytest.approx(-74.0060)
        assert chart.house_system == HouseSystem.WHOLE_SIGN
        assert chart.ascendant == pytest.approx(123.45)
        assert chart.midheaven == pytest.approx(234.56)
        assert len(chart.house_cusps) == 12
        assert chart.seed == 987654321
        assert chart.dominant_element == "fire"

    def test_chart_immutability(self, sample_date, sample_location) -> None:
        chart = Chart(
            date=sample_date,
            latitude=sample_location["lat"],
            longitude=sample_location["lon"],
            house_system=HouseSystem.WHOLE_SIGN,
            planetary_positions={},
            ascendant=0.0,
            midheaven=0.0,
            house_cusps=[],
            seed=0,
            dominant_element="earth",
        )
        with pytest.raises((FrozenInstanceError, TypeError)):
            chart.date = date(2026, 1, 1)  # pyright: ignore[reportAttributeAccessIssue]

    def test_chart_has_all_required_fields(self) -> None:
        field_names = {f.name for f in fields(Chart)}
        expected = {
            "date",
            "latitude",
            "longitude",
            "house_system",
            "planetary_positions",
            "ascendant",
            "midheaven",
            "house_cusps",
            "seed",
            "dominant_element",
        }
        assert expected == field_names


class TestPlanetaryPositionDataclass:
    def test_planetary_position_is_dataclass(self) -> None:
        assert is_dataclass(PlanetaryPosition)

    def test_planetary_position_creation(self) -> None:
        pp = PlanetaryPosition(
            body="sun",
            longitude=285.5,
            zodiac_sign=None,  # type: ignore[arg-type]
        )
        assert pp.body == "sun"
        assert pp.longitude == pytest.approx(285.5)

    def test_planetary_position_immutability(self) -> None:
        pp = PlanetaryPosition(
            body="moon",
            longitude=100.0,
            zodiac_sign=None,  # type: ignore[arg-type]
        )
        with pytest.raises((FrozenInstanceError, TypeError)):
            pp.longitude = 200.0  # pyright: ignore[reportAttributeAccessIssue]


class TestCardPositionDataclass:
    def test_card_position_is_dataclass(self) -> None:
        assert is_dataclass(CardPosition)

    def test_card_position_with_required_fields(self) -> None:
        card = Card(name="The Fool", arcana=Arcana.MAJOR, keywords=("beginnings",))
        cp = CardPosition(
            position_label="Theme",
            card=card,
        )
        assert cp.position_label == "Theme"
        assert cp.card is card
        assert cp.house_number is None
        assert cp.resonant_planet is None
        assert cp.resonant_sign is None

    def test_card_position_with_all_fields(self) -> None:
        from orbpondering.constants import ZodiacSign

        card = Card(name="Ace of Wands", arcana=Arcana.MINOR, suit=Suit.WANDS, number=1)
        cp = CardPosition(
            position_label="Challenge",
            card=card,
            house_number=5,
            resonant_planet="mars",
            resonant_sign=ZodiacSign.ARIES,
        )
        assert cp.position_label == "Challenge"
        assert cp.house_number == 5
        assert cp.resonant_planet == "mars"
        assert cp.resonant_sign == ZodiacSign.ARIES


class TestTarotReadingDataclass:
    def test_tarot_reading_is_dataclass(self) -> None:
        assert is_dataclass(TarotReading)

    def test_tarot_reading_creation(self, sample_date) -> None:
        spread = Spread(name="Daily", positions=("Theme",))
        card = Card(name="The Sun", arcana=Arcana.MAJOR, keywords=("positivity",))
        cp = CardPosition(position_label="Theme", card=card)
        reading = TarotReading(
            date=sample_date,
            house_system=HouseSystem.EQUAL,
            spread=spread,
            seed=12345,
            positions=[cp],
        )
        assert reading.date == sample_date
        assert reading.house_system == HouseSystem.EQUAL
        assert reading.spread is spread
        assert reading.seed == 12345
        assert len(reading.positions) == 1
        assert reading.chart is None

    def test_tarot_reading_with_chart(self, sample_date) -> None:
        spread = Spread(name="Daily", positions=("Theme",))
        card = Card(name="The Sun", arcana=Arcana.MAJOR, keywords=("positivity",))
        cp = CardPosition(position_label="Theme", card=card)
        chart = Chart(
            date=sample_date,
            latitude=0.0,
            longitude=0.0,
            house_system=HouseSystem.WHOLE_SIGN,
            planetary_positions={},
            ascendant=0.0,
            midheaven=0.0,
            house_cusps=[],
            seed=12345,
            dominant_element="fire",
        )
        reading = TarotReading(
            date=sample_date,
            house_system=HouseSystem.WHOLE_SIGN,
            spread=spread,
            seed=12345,
            positions=[cp],
            chart=chart,
        )
        assert reading.chart is chart

    def test_tarot_reading_immutability(self, sample_date) -> None:
        spread = Spread(name="Daily", positions=("Theme",))
        card = Card(name="The Sun", arcana=Arcana.MAJOR, keywords=("positivity",))
        cp = CardPosition(position_label="Theme", card=card)
        reading = TarotReading(
            date=sample_date,
            house_system=HouseSystem.EQUAL,
            spread=spread,
            seed=12345,
            positions=[cp],
            chart=None,
        )
        with pytest.raises((FrozenInstanceError, TypeError)):
            reading.seed = 99999  # pyright: ignore[reportAttributeAccessIssue]

    def test_tarot_reading_chart_is_optional(self, sample_date) -> None:
        spread = Spread(name="Daily", positions=("Theme",))
        card = Card(name="The Sun", arcana=Arcana.MAJOR, keywords=("positivity",))
        cp = CardPosition(position_label="Theme", card=card)
        reading = TarotReading(
            date=sample_date,
            house_system=HouseSystem.EQUAL,
            spread=spread,
            seed=12345,
            positions=[cp],
            chart=None,
        )
        assert reading.chart is None
