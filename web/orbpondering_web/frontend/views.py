"""Frontend views."""

from datetime import date, datetime

from django.shortcuts import render
from orbpondering.constants import HouseSystem
from orbpondering.draw import birth_tarot_draw, tarot_draw_for_date
from orbpondering.models import BirthData


def _position_context(pos):
    """Convert a CardPosition to template-friendly dict."""
    card = pos.card
    entry = {
        "label": pos.position_label,
        "card": {
            "name": card.name,
            "arcana": card.arcana.value,
            "upright": card.upright,
            "number": card.number,
        },
        "house_number": pos.house_number,
    }
    if card.suit:
        entry["card"]["suit"] = card.suit.full_name
        entry["card"]["element"] = card.suit.element
        entry["card"]["suit_symbol"] = card.suit.symbol
    if card.keywords:
        entry["card"]["keywords"] = list(card.keywords)
    return entry


def index(request):
    """Landing page."""
    return render(request, "frontend/index.html", {"today": date.today().isoformat()})


def reading_view(request):
    """Display reading form or process submission."""
    today = date.today().isoformat()

    if request.method == "GET":
        return render(request, "frontend/reading_form.html", {"today": today})

    # POST — calculate reading
    try:
        d = datetime.strptime(request.POST.get("date", today), "%Y-%m-%d").date()
    except ValueError:
        d = date.today()

    try:
        lat = float(request.POST.get("lat", "0.0"))
    except ValueError:
        lat = 0.0

    try:
        lon = float(request.POST.get("lon", "0.0"))
    except ValueError:
        lon = 0.0

    house_str = request.POST.get("house_system", "whole_sign")
    try:
        house_system = HouseSystem(house_str)
    except ValueError:
        house_system = HouseSystem.WHOLE_SIGN

    spread = request.POST.get("spread", "daily")
    reversed_cards = request.POST.get("reversed") == "on"

    birth_date_str = request.POST.get("birth_date", "")
    use_natal = bool(birth_date_str)

    if use_natal:
        try:
            bd = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            bd = None

        bt = None
        bt_str = request.POST.get("birth_time", "")
        if bt_str:
            try:
                bt = datetime.strptime(bt_str, "%H:%M").time()
            except ValueError:
                pass

        try:
            blt = float(request.POST.get("birth_lat", "0.0"))
        except ValueError:
            blt = 0.0

        try:
            blo = float(request.POST.get("birth_lon", "0.0"))
        except ValueError:
            blo = 0.0

        btz = request.POST.get("birth_tz", "") or None

        if bd:
            birth_data = BirthData(date=bd, time=bt, lat=blt, lon=blo, tz=btz)
            reading = birth_tarot_draw(
                d=d, lat=lat, lon=lon, birth_data=birth_data,
                house_system=house_system, spread_name=spread,
                reversed_cards=reversed_cards,
            )
        else:
            reading = tarot_draw_for_date(
                d=d, lat=lat, lon=lon, house_system=house_system,
                spread_name=spread, reversed_cards=reversed_cards,
            )
    else:
        reading = tarot_draw_for_date(
            d=d, lat=lat, lon=lon, house_system=house_system,
            spread_name=spread, reversed_cards=reversed_cards,
        )

    context = _build_reading_context(reading)
    context["today"] = today
    is_htmx = request.headers.get("HX-Request") == "true"
    template = "_reading_results.html" if is_htmx else "reading_result.html"
    return render(request, f"frontend/{template}", context)


def _build_reading_context(reading):
    """Build template context from a TarotReading."""
    ctx = {
        "reading": {
            "date": reading.date.isoformat(),
            "house_system": reading.house_system.value,
            "seed": reading.seed,
            "spread": {
                "name": reading.spread.name,
                "positions": list(reading.spread.positions),
            },
            "positions": [_position_context(p) for p in reading.positions],
        }
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
                "degree": round(ppos.longitude % 30, 1),
            }
        ctx["reading"]["chart"] = {
            "date": chart.date.isoformat(),
            "ascendant": round(chart.ascendant, 1),
            "midheaven": round(chart.midheaven, 1),
            "dominant_element": chart.dominant_element,
            "planets": planets,
        }

    if reading.natal_chart:
        ctx["reading"]["natal_chart"] = {
            "birth_date": reading.natal_chart.birth_data.date.isoformat(),
        }

    if reading.aspects:
        ctx["reading"]["aspects"] = [
            {
                "natal_body": a.natal_body,
                "transit_body": a.transit_body,
                "aspect_type": a.aspect_type.value,
                "orb": round(a.orb, 1),
            }
            for a in reading.aspects
        ]

    return ctx
