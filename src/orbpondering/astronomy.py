"""Planetary and astronomical calculations using astropy."""

from __future__ import annotations

from datetime import date, datetime

import numpy as np
from astropy import units as u
from astropy.coordinates import get_body, get_sun, solar_system_ephemeris
from astropy.time import Time

from orbpondering.utils import _normalize

solar_system_ephemeris.set("jpl")


def _to_time(d: date | datetime, tz: str | None = None) -> Time:
    """Convert date or datetime to Astropy Time object."""
    if isinstance(d, datetime):
        # Already a datetime, ensure it has timezone info
        if d.tzinfo is None:
            # Assume UTC if no timezone
            return Time(d, scale="utc")
        return Time(d, scale="utc")
    # Date only - use noon UTC
    return Time(datetime(d.year, d.month, d.day, 12, 0, 0), scale="utc")


def sun_longitude(d: date | datetime, tz: str | None = None) -> float:
    t = _to_time(d, tz)
    sun = get_sun(t)
    ecliptic = sun.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def moon_longitude(d: date | datetime, tz: str | None = None) -> float:
    t = _to_time(d, tz)
    body = get_body("moon", t)
    ecliptic = body.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def _planet_longitude(name: str, d: date | datetime, tz: str | None = None) -> float:
    t = _to_time(d, tz)
    body = get_body(name, t)
    ecliptic = body.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def planetary_positions(d: date | datetime, tz: str | None = None) -> dict[str, float]:
    return {
        "sun": sun_longitude(d, tz),
        "moon": moon_longitude(d, tz),
        "mercury": _planet_longitude("mercury", d, tz),
        "venus": _planet_longitude("venus", d, tz),
        "mars": _planet_longitude("mars", d, tz),
        "jupiter": _planet_longitude("jupiter", d, tz),
        "saturn": _planet_longitude("saturn", d, tz),
        "uranus": _planet_longitude("uranus", d, tz),
        "neptune": _planet_longitude("neptune", d, tz),
        "pluto": _planet_longitude("pluto", d, tz),
    }


def sidereal_time(d: date | datetime, lon: float, tz: str | None = None) -> float:
    t = _to_time(d, tz)
    lst = t.sidereal_time("mean", longitude=lon * u.deg)
    return _normalize(float(lst.hour * 15.0))


def ascendant(
    d: date | datetime, lat: float, lon: float, tz: str | None = None
) -> float:
    t = _to_time(d, tz)
    lst_deg = t.sidereal_time("mean", longitude=lon * u.deg).deg
    lst_rad = np.deg2rad(lst_deg)
    lat_rad = np.deg2rad(lat)
    epsilon = np.deg2rad(23.438)

    sin_lst = np.sin(lst_rad)
    cos_lst = np.cos(lst_rad)
    tan_lat = np.tan(lat_rad)
    sin_eps = np.sin(epsilon)
    cos_eps = np.cos(epsilon)

    y = -cos_lst
    x = sin_lst * cos_eps + tan_lat * sin_eps
    return _normalize(np.rad2deg(np.arctan2(y, x)))


def midheaven(
    d: date | datetime, lat: float, lon: float, tz: str | None = None
) -> float:
    t = _to_time(d, tz)
    lst_deg = t.sidereal_time("mean", longitude=lon * u.deg).deg
    lst_rad = np.deg2rad(lst_deg)
    epsilon = 23.438

    y = np.cos(lst_rad)
    x = -np.sin(lst_rad) * np.tan(np.deg2rad(epsilon))
    mc_val = np.rad2deg(np.arctan2(y, x))
    return _normalize(mc_val)
