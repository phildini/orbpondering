"""Astrology utility functions for education mode."""

from __future__ import annotations

from orbpondering.constants import ZodiacSign


def zodiac_sign_for_degree(deg: float) -> ZodiacSign:
    """Map ecliptic longitude to zodiac sign."""
    normalized = deg % 360.0
    for sign in ZodiacSign:
        if sign.start_deg <= normalized < sign.end_deg:
            return sign
    # Should not happen, but fallback
    return ZodiacSign.PISCES


def get_planetary_rulerships() -> dict[str, list[str]]:
    """Return traditional planetary rulerships."""
    return {
        "fire": ["aries", "sagittarius", "leo"],
        "earth": ["taurus", "virgo", "capricorn"],
        "air": ["gemini", "libra", "aquarius"],
        "water": ["cancer", "scorpio", "pisces"],
    }


def get_planetary_exaltations() -> dict[str, str]:
    """Return planetary exaltations."""
    return {
        "sun": "aquarius",
        "moon": "cancer",
        "mercury": "virgo",
        "venus": "pisces",
        "mars": "scorpio",
        "jupiter": "pisces",
        "saturn": "capricorn",
        "uranus": "aries",
        "neptune": "pisces",
        "pluto": "scorpio",
    }
