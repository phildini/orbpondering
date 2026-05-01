"""Main API: draw tarot spreads seeded by daily astrology."""

from __future__ import annotations

import random
from datetime import date

from orbpondering.cards import DECK, Card
from orbpondering.constants import HouseSystem
from orbpondering.seed import chart_seed
from orbpondering.spreads import Spread, get_spread


def _shuffle_and_deal(
    seed: int, spread: Spread
) -> list[tuple[str, Card]]:
    rng = random.Random(seed)
    cards = list(DECK)
    rng.shuffle(cards)
    drawn = cards[: len(spread.positions)]
    return list(zip(spread.positions, drawn, strict=True))


def daily_tarot_draw(
    d: date,
    lat: float,
    lon: float,
    house_system: HouseSystem,
    spread: Spread,
) -> dict:
    seed = chart_seed(d, lat, lon, house_system)
    positions = _shuffle_and_deal(seed, spread)
    return {
        "seed": seed,
        "spread": spread,
        "date": d,
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "positions": [
            {"position_label": label, "card": card}
            for label, card in positions
        ],
    }


def tarot_draw_for_date(
    d: date,
    lat: float = 0.0,
    lon: float = 0.0,
    house_system: HouseSystem = HouseSystem.WHOLE_SIGN,
    spread_name: str = "daily",
) -> dict:
    spread = get_spread(spread_name)
    return daily_tarot_draw(d, lat, lon, house_system, spread)
