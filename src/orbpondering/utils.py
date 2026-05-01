"""Shared utility functions for orbpondering."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orbpondering.constants import ZodiacSign


def _normalize(deg: float) -> float:
    """Normalize degrees to [0, 360)."""
    return float(deg % 360.0)


def zodiac_sign_for_degree(deg: float) -> ZodiacSign:
    """Map ecliptic longitude to zodiac sign."""
    from orbpondering.constants import ZodiacSign
    
    normalized = deg % 360.0
    for sign in ZodiacSign:
        if sign.start_deg <= normalized < sign.end_deg:
            return sign
    # Should not happen, but fallback
    return ZodiacSign.PISCES


PLANET_SYMBOLS = {
    "sun": "\u2609",
    "moon": "\u263D", 
    "mercury": "\u263F",
    "venus": "\u2640",
    "mars": "\u2642",
    "jupiter": "\u2643",
    "saturn": "\u2644",
    "uranus": "\u2645",
    "neptune": "\u2646",
    "pluto": "\u2647",
}
