"""Deterministic seed generation from astrological chart data."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orbpondering.models import NatalChart, Chart
    from orbpondering.constants import HouseSystem

from orbpondering.astronomy import planetary_positions
from orbpondering.houses import house_cusps


def chart_seed(
    d: date | datetime, lat: float, lon: float, house_system: HouseSystem,
    natal_chart: NatalChart | None = None,
    aspects: tuple[Aspect, ...] = (),
    tz: str | None = None,
) -> int:
    """Generate a deterministic integer seed from the day's astrological chart."""
    positions = planetary_positions(d, tz)
    cusps = house_cusps(d, lat, lon, house_system)

    raw = {
        "date": d.isoformat() if isinstance(d, datetime) else d.isoformat(),
        "lat": lat,
        "lon": lon,
        "house_system": house_system.value,
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
