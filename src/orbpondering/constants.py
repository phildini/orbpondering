"""Core enums and constants for orbpondering."""

from __future__ import annotations

from enum import Enum


class HouseSystem(Enum):
    """Supported astrological house systems."""

    WHOLE_SIGN = "whole_sign"
    EQUAL = "equal"
    PORPHYRY = "porphyry"
    PLACIDUS = "placidus"


class ZodiacSign(Enum):
    """The 12 zodiac signs with ecliptic longitude ranges."""

    ARIES = (0, 30, "Aries", "\u2648", "fire", "cardinal")
    TAURUS = (30, 60, "Taurus", "\u2649", "earth", "fixed")
    GEMINI = (60, 90, "Gemini", "\u264A", "air", "mutable")
    CANCER = (90, 120, "Cancer", "\u264B", "water", "cardinal")
    LEO = (120, 150, "Leo", "\u264C", "fire", "fixed")
    VIRGO = (150, 180, "Virgo", "\u264D", "earth", "mutable")
    LIBRA = (180, 210, "Libra", "\u264E", "air", "cardinal")
    SCORPIO = (210, 240, "Scorpio", "\u264F", "water", "fixed")
    SAGITTARIUS = (240, 270, "Sagittarius", "\u2650", "fire", "mutable")
    CAPRICORN = (270, 300, "Capricorn", "\u2651", "earth", "cardinal")
    AQUARIUS = (300, 330, "Aquarius", "\u2652", "air", "fixed")
    PISCES = (330, 360, "Pisces", "\u2653", "water", "mutable")

    def __init__(
        self,
        start_deg: float,
        end_deg: float,
        full_name: str,
        symbol: str,
        element: str,
        modality: str,
    ) -> None:
        self.start_deg = start_deg
        self.end_deg = end_deg
        self.full_name = full_name
        self.symbol = symbol
        self.element = element
        self.modality = modality


class Arcana(Enum):
    """Major vs Minor Arcana."""

    MAJOR = "major"
    MINOR = "minor"


class Suit(Enum):
    """The four suits of the Minor Arcana."""

    WANDS = ("wands", "fire", "\u26A1")
    CUPS = ("cups", "water", "\u2617")
    SWORDS = ("swords", "air", "\u2694")
    PENTACLES = ("pentacles", "earth", "\u2B50")

    def __init__(self, full_name: str, element: str, symbol: str) -> None:
        self.full_name = full_name
        self.element = element
        self.symbol = symbol


class AspectType(Enum):
    """Classical astrological aspects."""

    CONJUNCTION = (0, 8)
    SEXTILE = (60, 6)
    SQUARE = (90, 8)
    TRINE = (120, 8)
    OPPOSITION = (180, 8)
