"""Core education mode execution engine."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date

from rich.console import Console

from orbpondering.constants import HouseSystem
from orbpondering.education.steps import (
    step_planetary_positions,
    step_sidereal_time,
    step_house_cusps,
    step_planets_in_houses,
    step_seed_generation,
    step_card_draw,
)


def run_education(
    date: date,
    lat: float,
    lon: float,
    house_system: HouseSystem,
    spread_name: str,
    console: Console,
    verbose: bool = False,
) -> dict:
    """Run all education steps sequentially and return final draw result."""
    # Initialize context
    ctx = {
        "date": date,
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread_name": spread_name,
    }
    
    # Run each step in sequence
    steps = [
        step_planetary_positions,
        step_sidereal_time,
        step_house_cusps,
        step_planets_in_houses,
        step_seed_generation,
        step_card_draw,
    ]
    
    for step in steps:
        step(console, ctx, verbose)
    
    return ctx.get("card_draw", {})
