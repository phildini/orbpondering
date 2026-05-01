from datetime import date

from orbpondering.astronomy import (
    ascendant,
    midheaven,
    moon_longitude,
    planetary_positions,
    sidereal_time,
    sun_longitude,
)


def test_sun_longitude_range() -> None:
    d = date(2025, 1, 15)
    lon = sun_longitude(d)
    assert 0 <= lon < 360


def test_moon_longitude_range() -> None:
    d = date(2025, 1, 15)
    lon = moon_longitude(d)
    assert 0 <= lon < 360


def test_planetary_positions_all_present() -> None:
    d = date(2025, 1, 15)
    pos = planetary_positions(d)
    assert len(pos) == 10
    assert all(0 <= v < 360 for v in pos.values())


def test_sidereal_time() -> None:
    d = date(2025, 1, 15)
    lst = sidereal_time(d, -74.0)
    assert 0 <= lst < 360


def test_ascendant_value() -> None:
    d = date(2025, 1, 15)
    asc = ascendant(d, 40.7, -74.0)
    assert 0 <= asc < 360


def test_midheaven_value() -> None:
    d = date(2025, 1, 15)
    mc = midheaven(d, 40.7, -74.0)
    assert 0 <= mc < 360
