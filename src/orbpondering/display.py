"""Rich-enhanced terminal display for tarot spreads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from orbpondering.constants import Arcana, HouseSystem, Suit

if TYPE_CHECKING:
    from orbpondering.models import TarotReading


def _get_suit_symbol(suit: Suit | None) -> str:
    if not suit:
        return ""
    return suit.symbol


def _get_house_symbol(house_system: HouseSystem) -> str:
    symbols = {
        HouseSystem.WHOLE_SIGN: "\u2B6D",
        HouseSystem.EQUAL: "\u2B6E",
        HouseSystem.PORPHYRY: "\u2B6F",
        HouseSystem.PLACIDUS: "\u2B70",
    }
    return symbols.get(house_system, "\u2B6D")


def display_reading(reading: TarotReading) -> None:
    try:
        from rich.console import Console
        from rich.table import Table
    except ImportError:
        raise ImportError(
            "Rich is required for display. Install with: pip install rich"
        ) from None

    console = Console()
    house_symbol = _get_house_symbol(reading.house_system)

    console.print(
        f"[bold blue]{reading.spread.name} for {reading.date}[/]",
        style="bold",
    )
    console.print(f"[cyan]House System:[/] {house_symbol} {reading.house_system.value}")
    console.print(f"[cyan]Seed:[/] {reading.seed:016x}")
    console.print()

    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Position", style="bold magenta", no_wrap=True)
    table.add_column("Card", style="bold white")
    table.add_column("Keywords", style="bright_green")

    for pos in reading.positions:
        position_label = f"[bold]{pos.position_label}[/]"
        card = pos.card

        if card.arcana == Arcana.MAJOR:
            card_name = card.name
        else:
            suit_symbol = _get_suit_symbol(card.suit)
            card_name = f"{suit_symbol} {card.name}"

        orientation = "\u2191" if card.upright else "\u2193"
        card_name += f" {orientation}"

        keywords = ", ".join(card.keywords) if card.keywords else "No keywords"
        table.add_row(position_label, card_name, keywords)

    console.print(table)
    console.print()
