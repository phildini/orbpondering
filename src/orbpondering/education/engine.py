"""Core education mode execution engine."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date

from rich.console import Console

from orbpondering.constants import HouseSystem
from orbpondering.education.steps import (
    step_card_draw,
    step_house_cusps,
    step_planetary_positions,
    step_planets_in_houses,
    step_seed_generation,
    step_sidereal_time,
)


def run_education(
    d: date,
    lat: float,
    lon: float,
    house_system: HouseSystem,
    spread_name: str,
    console: Console,
    verbose: bool = False,
) -> dict:
    ctx: dict = {
        "date": d,
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread_name": spread_name,
    }

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
