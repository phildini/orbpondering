"""Educational content and meanings."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orbpondering.constants import ZodiacSign


HOUSE_MEANINGS = {
    1: "Self, identity, physical body, first impressions",
    2: "Resources, possessions, self-worth, values",
    3: "Communication, siblings, short trips, learning",
    4: "Home, family, roots, private life",
    5: "Creativity, romance, children, self-expression",
    6: "Daily routines, health, service, work",
    7: "Partnerships, contracts, open enemies, marriage",
    8: "Transformation, shared resources, death/rebirth, taboos",
    9: "Higher learning, philosophy, travel, spirituality",
    10: "Career, public image, authority, life direction",
    11: "Friendships, groups, hopes, future vision",
    12: "Subconscious, retreat, secrets, endings",
}

ELEMENT_MEANINGS = {
    "fire": "Energy, passion, will, action, inspiration",
    "earth": "Stability, material world, practicality, nature",
    "air": "Intellect, communication, ideas, social connection", 
    "water": "Emotion, intuition, feelings, subconscious",
}

PLANETARY_MEANINGS = {
    "sun": "Core identity, ego, vitality, creative force",
    "moon": "Emotions, subconscious, habits, nurturing",
    "mercury": "Communication, intellect, logic, movement",
    "venus": "Love, beauty, values, harmony, attraction",
    "mars": "Action, drive, aggression, energy, desire",
    "jupiter": "Expansion, abundance, luck, philosophy",
    "saturn": "Structure, discipline, limitation, responsibility",
    "uranus": "Innovation, sudden change, technology, rebellion",
    "neptune": "Dreams, illusion, spirituality, creativity, dissolution",
    "pluto": "Transformation, power, regeneration, depth",
}

SPREAD_POSITIONS = {
    "daily": {"Theme": "The dominant energy shaping today"},
    "three_card": {
        "Past": "What has shaped the current moment",
        "Present": "The energy available right now",
        "Future": "Where things are headed if current patterns continue",
    },
    "celtic_cross": {
        "Present": "Your current situation",
        "Challenge": "What's blocking or testing you",
        "Past": "Recent history influencing now",
        "Future": "Near-future outcome",
        "Conscious": "What you're aware of",
        "Unconscious": "Hidden factors",
        "Querent": "Your attitude toward the situation",
        "Environment": "External influences",
        "Hopes": "What you're hoping for or fearing",
        "Outcome": "Final result if things stay as they are",
    },
}

def get_house_meanings() -> dict[int, str]:
    """Return house meanings mapping."""
    return HOUSE_MEANINGS.copy()

def get_element_meanings() -> dict[str, str]:
    """Return element meanings mapping."""
    return ELEMENT_MEANINGS.copy()

def get_planetary_meanings() -> dict[str, str]:
    """Return planetary meanings mapping."""
    return PLANETARY_MEANINGS.copy()

def get_spread_positions(spread_name: str) -> dict[str, str]:
    """Return position meanings for a specific spread."""
    return SPREAD_POSITIONS.get(spread_name, {}).copy()
