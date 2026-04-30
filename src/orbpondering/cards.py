"""All 78 tarot cards with suit, rank, keywords, and arcana type."""

from __future__ import annotations

from dataclasses import dataclass

from orbpondering.constants import Arcana, Suit


@dataclass(frozen=True)
class Card:
    name: str
    arcana: Arcana
    suit: Suit | None = None
    number: int | None = None
    keywords: tuple[str, ...] = ()


MAJOR_ARCANA: tuple[Card, ...] = tuple(
    Card(name=name, arcana=Arcana.MAJOR, keywords=keywords)
    for name, keywords in [
        ("The Fool", ("beginnings", "innocence", "spontaneity")),
        ("The Magician", ("power", "action", "concentration")),
        ("The High Priestess", ("intuition", "unconscious", "mystery")),
        ("The Empress", ("fertility", "nurture", "abundance")),
        ("The Emperor", ("authority", "structure", "control")),
        ("The Hierophant", ("tradition", "conformity", "morality")),
        ("The Lovers", ("love", "harmony", "relationships")),
        ("The Chariot", ("control", "willpower", "success")),
        ("Strength", ("strength", "courage", "persuasion")),
        ("The Hermit", ("introspection", "guidance", "solitude")),
        ("Wheel of Fortune", ("cycles", "change", "fate")),
        ("Justice", ("justice", "fairness", "truth")),
        ("The Hanged Man", ("pause", "surrender", "new_perspective")),
        ("Death", ("endings", "change", "transformation")),
        ("Temperance", ("balance", "moderation", "patience")),
        ("The Devil", ("shadow", "attachment", "restriction")),
        ("The Tower", ("sudden_change", "upheaval", "chaos")),
        ("The Star", ("hope", "faith", "purpose")),
        ("The Moon", ("illusion", "fear", "anxiety")),
        ("The Sun", ("positivity", "fun", "warmth")),
        ("Judgement", ("judgement", "rebirth", "inner_calling")),
        ("The World", ("completion", "integration", "accomplishment")),
    ]
)

_MINOR_RANKS: list[tuple[str, int, tuple[str, ...]]] = [
    ("Ace", 1, ("beginning", "potential", "opportunity")),
    ("Two", 2, ("balance", "choice", "conflict")),
    ("Three", 3, ("growth", "creativity", "expression")),
    ("Four", 4, ("stability", "foundation", "structure")),
    ("Five", 5, ("change", "challenge", "conflict")),
    ("Six", 6, ("harmony", "cooperation", "communication")),
    ("Seven", 7, ("mystery", "assessment", "patience")),
    ("Eight", 8, ("movement", "focus", "mastery")),
    ("Nine", 9, ("culmination", "fulfillment", "achievement")),
    ("Ten", 10, ("completion", "cycle", "endings")),
    ("Page", 11, ("curiosity", "exploration", "message")),
    ("Knight", 12, ("action", "movement", "passion")),
    ("Queen", 13, ("nurturing", "intuition", "wisdom")),
    ("King", 14, ("authority", "structure", "mastery")),
]

MINOR_ARCANA: tuple[Card, ...] = tuple(
    Card(
        name=f"{rank} of {suit.name.title()}",
        arcana=Arcana.MINOR,
        suit=suit,
        number=num,
        keywords=key,
    )
    for suit in Suit
    for rank, num, key in _MINOR_RANKS
)

DECK: tuple[Card, ...] = MAJOR_ARCANA + MINOR_ARCANA
