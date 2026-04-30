"""House cusp calculations for four house systems."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date

from orbpondering.astronomy import ascendant, midheaven
from orbpondering.constants import HouseSystem


def _normalize(deg: float) -> float:
    return float(deg % 360.0)


def whole_sign_cusps(asc_deg: float) -> list[float]:
    sign_index = int(asc_deg // 30)
    first_cusp = sign_index * 30.0
    return [_normalize(first_cusp + i * 30.0) for i in range(12)]


def equal_cusps(asc_deg: float) -> list[float]:
    return [_normalize(asc_deg + i * 30.0) for i in range(12)]


def porphyry_cusps(asc_deg: float, mc_deg: float) -> list[float]:
    ic_deg = (mc_deg + 180.0) % 360.0
    desc_deg = (asc_deg + 180.0) % 360.0

    def _quadrant(start: float, end: float) -> list[float]:
        diff = (end - start) % 360.0
        return [
            _normalize(start),
            _normalize(start + diff / 3.0),
            _normalize(start + 2.0 * diff / 3.0),
        ]

    q1 = _quadrant(asc_deg, ic_deg)
    q2 = _quadrant(ic_deg, desc_deg)
    q3 = _quadrant(desc_deg, mc_deg)
    q4 = _quadrant(mc_deg, asc_deg)

    return q1 + q2 + q3 + q4


def _placidus_cusps(asc_deg: float, mc_deg: float) -> list[float]:
    return porphyry_cusps(asc_deg, mc_deg)


def house_cusps(
    d: date, lat: float, lon: float, house_system: HouseSystem
) -> list[float]:
    asc = ascendant(d, lat, lon)
    mc = midheaven(d, lat, lon)

    handlers: dict[HouseSystem, Callable[[float, float], list[float]]] = {
        HouseSystem.WHOLE_SIGN: lambda a, m: whole_sign_cusps(a),
        HouseSystem.EQUAL: lambda a, m: equal_cusps(a),
        HouseSystem.PORPHYRY: porphyry_cusps,
        HouseSystem.PLACIDUS: _placidus_cusps,
    }

    return handlers[house_system](asc, mc)
