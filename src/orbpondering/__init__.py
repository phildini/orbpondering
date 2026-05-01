"""orbpondering - Tarot spreads seeded by daily astrological calculations."""

from __future__ import annotations

from orbpondering.cards import DECK, MAJOR_ARCANA, MINOR_ARCANA, Card
from orbpondering.constants import Arcana, HouseSystem, Suit, ZodiacSign
from orbpondering.draw import daily_tarot_draw, tarot_draw_for_date
from orbpondering.seed import chart_seed
from orbpondering.spreads import Spread, get_spread

__all__ = [
    "Arcana",
    "Card",
    "DECK",
    "HouseSystem",
    "MAJOR_ARCANA",
    "MINOR_ARCANA",
    "Spread",
    "Suit",
    "ZodiacSign",
    "chart_seed",
    "daily_tarot_draw",
    "get_spread",
    "tarot_draw_for_date",
]

__version__ = "0.1.0"
