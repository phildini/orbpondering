"""Spread definitions for tarot reads."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Spread:
    name: str
    positions: tuple[str, ...]


SPREADS: dict[str, Spread] = {
    "daily": Spread(
        name="Tarot of the Day",
        positions=("Theme",),
    ),
    "three_card": Spread(
        name="Three Card Spread",
        positions=("Past", "Present", "Future"),
    ),
    "celtic_cross": Spread(
        name="Celtic Cross",
        positions=(
            "Present",
            "Challenge",
            "Past",
            "Future",
            "Conscious",
            "Unconscious",
            "Querent",
            "Environment",
            "Hopes",
            "Outcome",
        ),
    ),
}


def get_spread(name: str) -> Spread:
    if name not in SPREADS:
        raise KeyError(
            f"Spread '{name}' not found. Available: {', '.join(SPREADS)}"
        )
    return SPREADS[name]
