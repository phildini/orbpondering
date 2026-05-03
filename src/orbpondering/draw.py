"""Main API: draw tarot spreads seeded by daily astrology."""

from __future__ import annotations

import random
from datetime import date, datetime

from orbpondering.aspects import find_aspects
from orbpondering.cards import DECK, Card
from orbpondering.constants import Arcana
from orbpondering.models import Chart, CardPosition, TarotReading
from orbpondering.seed import chart_seed
from orbpondering.spreads import Spread, get_spread
from orbpondering.utils import zodiac_sign_for_degree


def _shuffle_and_deal(
    seed: int, spread: Spread
) -> list[tuple[str, Card]]:
    rng = random.Random(seed)
    cards = list(DECK)
    rng.shuffle(cards)
    drawn = cards[: len(spread.positions)]
    return list(zip(spread.positions, drawn, strict=True))


def _infer_house_index(
    card: Card,
    chart: Chart,
) -> int | None:
    if card.arcana == Arcana.MAJOR or card.suit is None:
        return None
    suit_element = card.suit.element
    for planet_pos in chart.planetary_positions.values():
        if planet_pos.zodiac_sign.element == suit_element:
            for house_idx, cusp in enumerate(chart.house_cusps):
                if cusp == planet_pos.longitude:
                    return house_idx
    return 0


def compute_chart(
    d: date | datetime,
    lat: float,
    lon: float,
    house_system,
    tz: str | None = None,
) -> Chart:
    from orbpondering.astronomy import (
        ascendant,
        midheaven,
        planetary_positions,
        sidereal_time,
    )
    from orbpondering.constants import HouseSystem
    from orbpondering.houses import house_cusps

    positions = planetary_positions(d, tz)
    asc = ascendant(d, lat, lon, tz)
    mc = midheaven(d, lat, lon, tz)
    sidereal_time(d, lon, tz)
    cusps = house_cusps(d, lat, lon, house_system)

    planetary_posns = {
        body: type("PlanetaryPosition", (), {
            "body": body,
            "longitude": deg,
            "zodiac_sign": zodiac_sign_for_degree(deg),
        })()
        for body, deg in positions.items()
    }

    elements = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    for deg in positions.values():
        sign = zodiac_sign_for_degree(deg)
        elements[sign.element] += 1
    dominant = max(elements, key=elements.get)

    seed = chart_seed(d, lat, lon, house_system, tz=tz)
    return Chart(
        date=d,
        latitude=lat,
        longitude=lon,
        house_system=house_system,
        planetary_positions=planetary_posns,
        ascendant=asc,
        midheaven=mc,
        house_cusps=cusps,
        seed=seed,
        dominant_element=dominant,
    )


def compute_natal_chart(birth_data) -> NatalChart:
    from orbpondering.astronomy import planetary_positions
    from orbpondering.models import NatalChart
    
    positions = planetary_positions(birth_data.date, birth_data.tz)
    return NatalChart(
        birth_data=birth_data,
        planetary_positions=positions,
    )


def daily_tarot_draw(
    d: date | datetime,
    lat: float,
    lon: float,
    house_system,
    spread: Spread,
    tz: str | None = None,
) -> TarotReading:
    seed = chart_seed(d, lat, lon, house_system, tz=tz)
    positions = _shuffle_and_deal(seed, spread)

    chart = compute_chart(d, lat, lon, house_system, tz)

    card_positions = []
    for label, card in positions:
        house_num = _infer_house_index(card, chart)
        card_positions.append(
            CardPosition(
                position_label=label,
                card=card,
                house_number=house_num,
            )
        )

    return TarotReading(
        date=d,
        house_system=house_system,
        spread=spread,
        seed=seed,
        positions=card_positions,
        chart=chart,
    )


def birth_tarot_draw(
    d: date | datetime,
    lat: float,
    lon: float,
    birth_data,
    house_system,
    spread_name: str,
) -> TarotReading:
    """Draw a tarot spread using the user's natal chart + current transits."""
    from orbpondering.models import NatalChart
    from orbpondering.spreads import get_spread
    
    spread = get_spread(spread_name)
    transit_chart = compute_chart(d, lat, lon, house_system, birth_data.tz)
    natal_chart = compute_natal_chart(birth_data)
    aspects = find_aspects(natal_chart, transit_chart)
    seed = chart_seed(
        d, lat, lon, house_system, natal_chart, aspects, birth_data.tz
    )
    positions = _shuffle_and_deal(seed, spread)

    # TODO: Use aspects for house assignment in card positions if desired
    card_positions = [
        CardPosition(position_label=label, card=card)
        for label, card in positions
    ]

    return TarotReading(
        date=d,
        house_system=house_system,
        spread=spread,
        seed=seed,
        positions=card_positions,
        chart=transit_chart,
        natal_chart=natal_chart,
        aspects=aspects,
    )


def tarot_draw_from_seed(
    seed: int,
    spread_name: str,
) -> TarotReading:
    from orbpondering.constants import HouseSystem
    
    spread = get_spread(spread_name)
    positions = _shuffle_and_deal(seed, spread)

    card_positions = [
        CardPosition(position_label=label, card=card)
        for label, card in positions
    ]

    return TarotReading(
        date=date.today(),
        house_system=HouseSystem.WHOLE_SIGN,
        spread=spread,
        seed=seed,
        positions=card_positions,
        chart=None,
    )


def tarot_draw_for_date(
    d: date,
    lat: float = 0.0,
    lon: float = 0.0,
    house_system=None,
    spread_name: str = "daily",
) -> TarotReading:
    from orbpondering.constants import HouseSystem
    from orbpondering.spreads import get_spread
    
    if house_system is None:
        house_system = HouseSystem.WHOLE_SIGN
    
    spread = get_spread(spread_name)
    return daily_tarot_draw(d, lat, lon, house_system, spread)
