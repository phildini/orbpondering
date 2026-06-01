"""API views for orbpondering calculations."""

from datetime import date, datetime

from orbpondering.constants import HouseSystem
from orbpondering.draw import birth_tarot_draw, tarot_draw_for_date
from orbpondering.models import BirthData, TarotReading
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import NatalReadingRequestSerializer, ReadingRequestSerializer

PLANET_MEANINGS = {
    "sun": "Core identity, ego, life force, vitality",
    "moon": "Emotions, intuition, subconscious, habits",
    "mercury": "Communication, thinking, travel, intellect",
    "venus": "Love, beauty, values, relationships, money",
    "mars": "Action, drive, desire, ambition, aggression",
    "jupiter": "Expansion, luck, wisdom, growth, optimism",
    "saturn": "Structure, discipline, responsibility, lessons, time",
    "uranus": "Change, innovation, rebellion, breakthroughs, freedom",
    "neptune": "Dreams, illusion, spirituality, intuition, confusion",
    "pluto": "Transformation, power, rebirth, depth, the unconscious",
}


def _reading_to_dict(reading: TarotReading) -> dict:
    """Convert a TarotReading dataclass to a JSON-safe dict."""
    positions = []
    for pos in reading.positions:
        card = pos.card
        card_dict = {
            "name": card.name,
            "arcana": card.arcana.value,
            "upright": card.upright,
        }
        if card.suit:
            card_dict["suit"] = card.suit.full_name
            card_dict["suit_symbol"] = card.suit.symbol
            card_dict["element"] = card.suit.element
        if card.number:
            card_dict["number"] = card.number
        if card.keywords:
            card_dict["keywords"] = list(card.keywords)

        positions.append({
            "label": pos.position_label,
            "card": card_dict,
            "house_number": pos.house_number,
        })

    result: dict = {
        "date": reading.date.isoformat(),
        "house_system": reading.house_system.value,
        "spread": {
            "name": reading.spread.name,
            "positions": list(reading.spread.positions),
        },
        "seed": reading.seed,
        "positions": positions,
    }

    if reading.chart:
        chart = reading.chart
        planets = {}
        for body, ppos in chart.planetary_positions.items():
            planets[body] = {
                "longitude": ppos.longitude,
                "sign": ppos.zodiac_sign.full_name,
                "sign_symbol": ppos.zodiac_sign.symbol,
                "element": ppos.zodiac_sign.element,
                "modality": ppos.zodiac_sign.modality,
                "degree": ppos.longitude % 30,
                "meaning": PLANET_MEANINGS.get(body, ""),
            }
        result["chart"] = {
            "date": chart.date.isoformat(),
            "latitude": chart.latitude,
            "longitude": chart.longitude,
            "house_system": chart.house_system.value,
            "ascendant": chart.ascendant,
            "midheaven": chart.midheaven,
            "house_cusps": chart.house_cusps,
            "seed": chart.seed,
            "dominant_element": chart.dominant_element,
            "planets": planets,
        }

    if reading.natal_chart:
        nc = reading.natal_chart
        result["natal_chart"] = {
            "birth_date": nc.birth_data.date.isoformat(),
            "planets": nc.planetary_positions,
        }

    if reading.aspects:
        result["aspects"] = [
            {
                "natal_body": a.natal_body,
                "transit_body": a.transit_body,
                "separation": a.separation,
                "aspect_type": a.aspect_type.value,
                "orb": round(a.orb, 1),
            }
            for a in reading.aspects if a.orb <= 3
        ]
        loose = sum(1 for a in reading.aspects if a.orb > 3)
        result["aspects_loose_count"] = loose

    return result


@api_view(["POST"])
def create_reading(request: Request) -> Response:
    """Draw a standard tarot reading for a date/location."""
    serializer = ReadingRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    d = data.get("date", date.today())
    house_system = HouseSystem(data["house_system"])

    reading = tarot_draw_for_date(
        d=d,
        lat=data["lat"],
        lon=data["lon"],
        house_system=house_system,
        spread_name=data["spread"],
        reversed_cards=data["reversed"],
    )

    return Response({"reading": _reading_to_dict(reading)})


@api_view(["POST"])
def create_natal_reading(request: Request) -> Response:
    """Draw a natal-chart-based tarot reading."""
    serializer = NatalReadingRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    d = data.get("date", date.today())
    house_system = HouseSystem(data["house_system"])

    birth_time = None
    if data.get("birth_time"):
        try:
            birth_time = datetime.strptime(data["birth_time"], "%H:%M").time()
        except ValueError:
            pass

    birth_data = BirthData(
        date=data["birth_date"],
        time=birth_time,
        lat=data["birth_lat"],
        lon=data["birth_lon"],
        tz=data.get("birth_tz") or None,
    )

    reading = birth_tarot_draw(
        d=d,
        lat=data["lat"],
        lon=data["lon"],
        birth_data=birth_data,
        house_system=house_system,
        spread_name=data["spread"],
        reversed_cards=data["reversed"],
    )

    return Response({"reading": _reading_to_dict(reading)})
