"""Card detail view modal for the TUI."""

from typing import Any

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from orbpondering.models import CardPosition


class CardDetailView(ModalScreen):
    """Modal screen showing detailed card information."""

    BINDINGS = [
        ("escape", "close", "Close"),
        ("p", "prev_card", "Previous"),
        ("n", "next_card", "Next"),
    ]

    def __init__(
        self, card_position: CardPosition, card_index: int = 0, total_cards: int = 1, **kwargs: Any
    ) -> None:
        """Initialize the card detail view."""
        super().__init__(**kwargs)
        self.card_position = card_position
        self.card_index = card_index
        self.total_cards = total_cards

    def compose(self) -> ComposeResult:
        """Compose the card detail view."""
        card = self.card_position.card
        element = self._get_element(card)

        yield Container(
            Vertical(
                Label(f"[b]{card.name}[/b]", id="card-detail-name"),
                Label(f"{card.arcana.value.title()} Arcana", id="card-detail-arcana"),
                Label(f"Position: {self.card_position.position_label}", id="card-detail-position"),
                Label(
                    f"Orientation: {'↓ Reversed' if not card.upright else '↑ Upright'}",
                    id="card-detail-orientation",
                ),
                id="card-detail-info",
            ),
            Vertical(
                Label("[b]Keywords:[/b]"),
                Static(", ".join(card.keywords), id="card-detail-keywords"),
                id="card-detail-keywords-section",
            ),
            Container(
                Label(f"[b]Element:[/b] {element}", id="card-detail-element"),
                id="card-detail-element-section",
            ),
            Container(
                Button("Previous", id="prev-card-btn", disabled=self.card_index == 0),
                Button("Next", id="next-card-btn", disabled=self.card_index >= self.total_cards - 1),
                Button("Close", id="close-btn"),
                id="card-detail-buttons",
            ),
            id="card-detail-container",
        )

    def _get_element(self, card: Any) -> str:
        """Get the element for a card."""
        if card.suit:
            element_icons = {
                "fire": "🔥 Fire",
                "water": "💧 Water",
                "air": "💨 Air",
                "earth": "🌍 Earth",
            }
            return element_icons.get(card.suit.element, "Unknown")
        return "Major Arcana (No element)"

    def action_close(self) -> None:
        """Close the modal."""
        self.dismiss()

    def action_prev_card(self) -> None:
        """Navigate to previous card."""
        if self.card_index > 0:
            self.post_message(CardDetailView.Navigate(self.card_index - 1))

    def action_next_card(self) -> None:
        """Navigate to next card."""
        if self.card_index < self.total_cards - 1:
            self.post_message(CardDetailView.Navigate(self.card_index + 1))

    class Navigate(Message):
        """Message sent when user wants to navigate to a different card."""

        def __init__(self, index: int) -> None:
            """Initialize the navigate message."""
            self.index = index
            super().__init__()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "close-btn":
            self.action_close()
        elif event.button.id == "prev-card-btn":
            self.action_prev_card()
        elif event.button.id == "next-card-btn":
            self.action_next_card()
