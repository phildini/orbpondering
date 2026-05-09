"""Education mode context management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from orbpondering.constants import HouseSystem


@dataclass
class EducationContext:
    """Shared state passed between education steps."""

    date: date
    lat: float
    lon: float
    house_system: HouseSystem
    spread_name: str
    planetary_positions: dict[str, float] | None = None
    ascendant: float | None = None
    midheaven: float | None = None
    house_cusps: list[float] | None = None
    planets_in_houses: dict[str, int] | None = None
    seed: int | None = None
    card_draw: dict | None = None
