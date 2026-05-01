"""Rich-enhanced terminal display for tarot spreads."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from orbpondering.constants import HouseSystem, Suit


def _get_suit_symbol(suit: Suit | None) -> str:
    """Get Unicode symbol for suit."""
    if not suit:
        return ""
    return suit.symbol


def _get_house_symbol(house_system: HouseSystem) -> str:
    """Get symbol representing house system."""
    symbols = {
        HouseSystem.WHOLE_SIGN: "⬭",
        HouseSystem.EQUAL: "⬮",
        HouseSystem.PORPHYRY: "⬯",
        HouseSystem.PLACIDUS: "⬰",
    }
    return symbols.get(house_system, "⬭")


def _get_card_orientation_indicator(card) -> str:
    """Get orientation indicator for card."""
    # Using simple Unicode arrows for orientation
    return "↑" if getattr(card, 'upright', True) else "↓"


def display_spread(draw_result) -> None:
    """Display a tarot spread in a rich, formatted console output."""
    console = Console()
    
    # Basic info section with symbols
    house_symbol = _get_house_symbol(draw_result['house_system'])
    console.print(f"[bold blue]Tarot Spread for {draw_result['date']}[/]", style="bold")
    console.print(f"[cyan]House System:[/] {house_symbol} {draw_result['house_system'].value}")
    console.print(f"[cyan]Spread:[/] {draw_result['spread'].name}")
    console.print(f"[cyan]Seed:[/] {draw_result['seed']:016x}")
    console.print()
    
    # Display positions and cards in a table
    table = Table(box=None, show_header=False, padding=(0, 1))
    table.add_column("Position", style="bold magenta", no_wrap=True)
    table.add_column("Card", style="bold white")
    table.add_column("Keywords", style="bright_green")
    
    for i, pos in enumerate(draw_result["positions"]):
        position_label = f"[bold]{pos['position_label']}[/]"
        card = pos["card"]
        
        # Build the card name with suit symbol and orientation
        if card.arcana == "major":
            card_name = card.name
        else:
            suit_symbol = _get_suit_symbol(card.suit)
            card_name = f"{suit_symbol} {card.name}"
        
        # Add orientation indicator
        orientation = _get_card_orientation_indicator(card)
        card_name += f" {orientation}"
        
        # Format keywords
        keywords = ", ".join(card.keywords) if card.keywords else "No keywords"
        
        table.add_row(position_label, card_name, keywords)
    
    console.print(table)
    console.print()
