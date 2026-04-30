"""Deterministic seed generation from astrological chart data."""

from __future__ import annotations

import hashlib
import json
from datetime import date

from orbpondering.astronomy import planetary_positions
from orbpondering.constants import HouseSystem
from orbpondering.houses import house_cusps


def chart_seed(
    d: date, lat: float, lon: float, house_system: HouseSystem
) -> int:
    """Generate a deterministic integer seed from the day's astrological chart."""
    positions = planetary_positions(d)
    cusps = house_cusps(d, lat, lon, house_system)

    raw = json.dumps(
        {
            "date": d.isoformat(),
            "lat": lat,
            "lon": lon,
            "house_system": house_system.value,
            "planets": positions,
            "cusps": cusps,
        },
        sort_keys=True,
    )

    h = hashlib.sha256(raw.encode("utf-8"))
    return int(h.hexdigest()[:16], 16)
