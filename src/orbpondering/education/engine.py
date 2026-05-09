"""Core education mode execution engine."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date

from rich.console import Console

from orbpondering.constants import HouseSystem
from orbpondering.education.steps import (
    step_aspects,
    step_birth_data,
    step_card_draw,
    step_house_cusps,
    step_natal_houses,
    step_natal_positions,
    step_planetary_positions,
    step_planets_in_houses,
    step_seed_generation,
    step_sidereal_time,
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


def run_education_with_natal(
    date: date,
    lat: float,
    lon: float,
    house_system: HouseSystem,
    spread_name: str,
    birth_data: BirthData,
    console: Console,
    verbose: bool = False,
) -> dict:
    """Run all education steps including natal chart and aspects."""
    # Initialize context
    ctx = {
        "date": date,
        "lat": lat,
        "lon": lon,
        "house_system": house_system,
        "spread_name": spread_name,
        "birth_data": birth_data,
    }

    # Run each step in sequence
    steps = [
        step_birth_data,
        step_natal_positions,
        step_natal_houses,
        step_planetary_positions,
        step_sidereal_time,
        step_house_cusps,
        step_planets_in_houses,
        step_aspects,
        step_seed_generation,
        step_card_draw,
    ]

    for step in steps:
        step(console, ctx, verbose)

    return ctx.get("card_draw", {})
