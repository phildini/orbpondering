"""Deterministic seed generation from astrological chart data."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime

from orbpondering.astronomy import planetary_positions
from orbpondering.constants import HouseSystem
from orbpondering.houses import house_cusps
from orbpondering.models import Aspect, NatalChart


def chart_seed(
    d: date | datetime,
    lat: float,
    lon: float,
    house_system: HouseSystem | str,
    natal_chart: NatalChart | None = None,
    aspects: tuple[Aspect, ...] = (),
    tz: str | None = None,
) -> int:
    """Generate a deterministic integer seed from the day's astrological chart."""
    positions = planetary_positions(d, tz)
    cusps = house_cusps(d, lat, lon, house_system)

    if isinstance(house_system, HouseSystem):
        house_system_key: str = house_system.value

    raw = {
        "date": d.isoformat() if isinstance(d, datetime) else d.isoformat(),
        "lat": lat,
        "lon": lon,
        "house_system": house_system_key,
        "planets": positions,
        "cusps": cusps,
    }

    if natal_chart:
        raw["natal_date"] = natal_chart.birth_data.date.isoformat()
        raw["natal_planets"] = natal_chart.planetary_positions
        raw["aspects"] = [
            (a.natal_body, a.transit_body, a.aspect_type.value[0], a.orb)
            for a in aspects
        ]

    raw_json = json.dumps(raw, sort_keys=True)
    h = hashlib.sha256(raw_json.encode("utf-8"))
    return int(h.hexdigest()[:16], 16)
