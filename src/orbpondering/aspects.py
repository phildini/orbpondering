"""Aspect detection and analysis for orbpondering."""

from __future__ import annotations

from typing import TYPE_CHECKING

from orbpondering.constants import AspectType
from orbpondering.models import Aspect


def _angular_separation(lon1: float, lon2: float) -> float:
    """Calculate the shortest angular distance between two longitudes."""
    diff = abs(lon1 - lon2) % 360
    return min(diff, 360 - diff)


def find_aspects(natal, transit) -> tuple[Aspect, ...]:
    """Detect classical aspects between all natal and transit planets."""
    aspects = []
    for natal_body, natal_lon in natal.planetary_positions.items():
        # Handle both raw floats and PlanetaryPosition objects
        if hasattr(natal_lon, 'longitude'):
            natal_lon = natal_lon.longitude
        for transit_body, transit_lon in transit.planetary_positions.items():
            # Handle both raw floats and PlanetaryPosition objects
            if hasattr(transit_lon, 'longitude'):
                transit_lon = transit_lon.longitude
            sep = _angular_separation(natal_lon, transit_lon)
            aspect_type, orb = _classify_aspect(sep)
            if aspect_type:
                aspects.append(
                    Aspect(
                        natal_body=natal_body,
                        transit_body=transit_body,
                        separation=sep,
                        aspect_type=aspect_type,
                        orb=orb,
                    )
                )
    # Sort by orb (tightest first)
    return tuple(sorted(aspects, key=lambda a: a.orb))


def _classify_aspect(separation: float) -> tuple[AspectType, float] | tuple[None, float]:
    """Classify an angular separation into an aspect."""
    for aspect_type in AspectType:
        ideal, max_orb = aspect_type.value
        orb = abs(separation - ideal)
        if orb <= max_orb:
            return aspect_type, orb
    return None, 0.0