"""Rich-enhanced terminal display for tarot spreads."""

from __future__ import annotations

from typing import TYPE_CHECKING

from orbpondering.constants import Arcana, HouseSystem, Suit
from orbpondering.utils import zodiac_sign_for_degree

if TYPE_CHECKING:
    from orbpondering.models import TarotReading



def _get_suit_symbol(suit: Suit | None) -> str:
    if not suit:
        return ""
    return suit.symbol


def _get_house_symbol(house_system: HouseSystem) -> str:
    house_system_key: str = str(house_system)
    symbols = {
        HouseSystem.WHOLE_SIGN.value: "\u2b6d",
        HouseSystem.EQUAL.value: "\u2b6e",
        HouseSystem.PORPHYRY.value: "\u2b6f",
        HouseSystem.PLACIDUS.value: "\u2b70",
    }
    return symbols.get(house_system_key, "\u2b6d")


def display_reading(reading: TarotReading) -> None:
    try:
        from rich.console import Console
        from rich.table import Table

        _use_rich = True
    except ImportError:
        _use_rich = False

    if _use_rich:
        console = Console()
        house_symbol = _get_house_symbol(reading.house_system)

        # Display natal chart summary if present
        if reading.natal_chart:
            natal = reading.natal_chart
            birth_data = natal.birth_data
            console.print(
                f"[bold blue]Natal Chart for {birth_data.date}[/]",
                style="bold",
            )
            # Show a few key positions
            key_planets = ["sun", "moon", "mercury", "venus", "mars"]
            natal_pos = natal.planetary_positions
            natal_parts = []
            for p in key_planets:
                if p in natal_pos:
                    sign = zodiac_sign_for_degree(natal_pos[p])
                    natal_parts.append(
                        f"{p[0].upper()} {sign.symbol} {sign.full_name[:3]}"
                    )
            console.print(
                f"  [cyan]Planets: [/][white]{', '.join(natal_parts)}[/]"
            )
            console.print()

        console.print(
            f"[bold blue]{reading.spread.name} for {reading.date}[/]",
            style="bold",
        )
        console.print(
            f"[cyan]House System:[/] {house_symbol} {reading.house_system}"
        )
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

            keywords = (
                ", ".join(card.keywords) if card.keywords else "No keywords"
            )
            table.add_row(position_label, card_name, keywords)

        console.print(table)
        console.print()
    else:
        # Fallback to plain text when Rich is unavailable
        house_symbol = _get_house_symbol(reading.house_system)

        if reading.natal_chart:
            natal = reading.natal_chart
            birth_data = natal.birth_data
            print(f"Natal Chart for {birth_data.date}")
            key_planets = ["sun", "moon", "mercury", "venus", "mars"]
            natal_pos = natal.planetary_positions
            natal_parts = []
            for p in key_planets:
                if p in natal_pos:
                    sign = zodiac_sign_for_degree(natal_pos[p])
                    natal_parts.append(
                        f"{p[0].upper()} {sign.symbol} {sign.full_name[:3]}"
                    )
            print(f"  Planets: {', '.join(natal_parts)}")
            print()

        print(f"{reading.spread.name} for {reading.date}")
        print(f"House System: {house_symbol} {reading.house_system}")
        print(f"Seed: {reading.seed:016x}")
        print()

        for pos in reading.positions:
            position_label = pos.position_label
            card = pos.card

            if card.arcana == Arcana.MAJOR:
                card_name = card.name
            else:
                suit_symbol = _get_suit_symbol(card.suit)
                card_name = f"{suit_symbol} {card.name}"

            orientation = "\u2191" if card.upright else "\u2193"
            card_name += f" {orientation}"

            keywords = (
                ", ".join(card.keywords) if card.keywords else "No keywords"
            )
            print(f"{position_label}: {card_name} ({keywords})")

        print()
