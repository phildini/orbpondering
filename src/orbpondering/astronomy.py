"""Planetary and astronomical calculations using astropy."""

from __future__ import annotations

from datetime import date, datetime

from astropy import units as u
from astropy.coordinates import EarthLocation, get_body, get_sun
from astropy.time import Time
import numpy as np


def _noon_utc(d: date) -> Time:
    return Time(datetime(d.year, d.month, d.day, 12, 0, 0), scale="utc")


def _normalize(deg: float) -> float:
    return float(deg % 360.0)


def sun_longitude(d: date) -> float:
    t = _noon_utc(d)
    sun = get_sun(t)
    ecliptic = sun.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def moon_longitude(d: date) -> float:
    t = _noon_utc(d)
    body = get_body("moon", t)
    ecliptic = body.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def _planet_longitude(name: str, d: date) -> float:
    t = _noon_utc(d)
    body = get_body(name, t)
    ecliptic = body.transform_to("geocentricmeanecliptic")
    return _normalize(float(ecliptic.lon.deg))


def planetary_positions(d: date) -> dict[str, float]:
    return {
        "sun": sun_longitude(d),
        "moon": moon_longitude(d),
        "mercury": _planet_longitude("mercury", d),
        "venus": _planet_longitude("venus", d),
        "mars": _planet_longitude("mars", d),
        "jupiter": _planet_longitude("jupiter", d),
        "saturn": _planet_longitude("saturn", d),
        "uranus": _planet_longitude("uranus", d),
        "neptune": _planet_longitude("neptune", d),
        "pluto": _planet_longitude("pluto", d),
    }


def sidereal_time(d: date, lon: float) -> float:
    t = _noon_utc(d)
    lst = t.sidereal_time("mean", longitude=lon * u.deg)
    return _normalize(float(lst.hour * 15.0))


def ascendant(d: date, lat: float, lon: float) -> float:
    t = _noon_utc(d)
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


def midheaven(d: date, lat: float, lon: float) -> float:
    t = _noon_utc(d)
    lst_deg = t.sidereal_time("mean", longitude=lon * u.deg).deg
    lst_rad = np.deg2rad(lst_deg)
    epsilon = 23.438

    y = np.cos(lst_rad)
    x = -np.sin(lst_rad) * np.tan(np.deg2rad(epsilon))
    mc_val = np.rad2deg(np.arctan2(y, x))
    return _normalize(mc_val)
