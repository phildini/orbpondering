"""Data models for orbpondering."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orbpondering.cards import Card
    from orbpondering.constants import AspectType, HouseSystem, ZodiacSign
    from orbpondering.spreads import Spread


@dataclass(frozen=True)
class PlanetaryPosition:
    """A celestial body's position in the zodiac."""
    body: str        # "sun", "moon", etc.
    longitude: float # degrees 0-360
    zodiac_sign: ZodiacSign


@dataclass(frozen=True)
class BirthData:
    """User's birth information."""
    date: date
    time: time | None  # None → noon UTC
    lat: float
    lon: float
    tz: str | None  # IANA timezone; None → UTC


@dataclass(frozen=True)
class Aspect:
    """Angular relationship between a natal and transit planet."""
    natal_body: str
    transit_body: str
    separation: float
    aspect_type: AspectType
    orb: float


@dataclass(frozen=True)
class NatalChart:
    """Complete natal astrological chart."""
    birth_data: BirthData
    planetary_positions: dict[str, float]

    @cached_property
    def house_cusps(self) -> dict[HouseSystem, list[float]]:
        """Compute all 4 house systems on first access."""
        from orbpondering.houses import house_cusps
        return {
            hs: house_cusps(
                self.birth_data.date,
                self.birth_data.lat,
                self.birth_data.lon,
                hs,
            )
            for hs in HouseSystem
        }


@dataclass(frozen=True)
class Chart:
    """Complete astrological chart for a given date and location."""
    date: date
    latitude: float
    longitude: float
    house_system: HouseSystem
    planetary_positions: dict[str, PlanetaryPosition]
    ascendant: float
    midheaven: float
    house_cusps: list[float]
    seed: int
    dominant_element: str  # fire/earth/air/water


@dataclass(frozen=True)
class CardPosition:
    """A card in its spread position."""
    position_label: str
    card: Card
    house_number: int | None = None
    resonant_planet: str | None = None
    resonant_sign: ZodiacSign | None = None


@dataclass(frozen=True)
class TarotReading:
    """Complete tarot reading result."""
    date: date
    house_system: HouseSystem
    spread: Spread
    seed: int
    positions: list[CardPosition]
    chart: Chart | None = None  # None if seeded manually
    natal_chart: NatalChart | None = None
    aspects: tuple[Aspect, ...] = ()
