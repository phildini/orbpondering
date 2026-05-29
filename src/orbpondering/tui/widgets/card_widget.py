"""Card widget for the TUI."""

from typing import Any

from textual import events
from textual.app import ComposeResult
from textual.widgets import Static

from orbpondering.models import CardPosition


class CardWidget(Static):
    """Widget to display a single tarot card in the TUI."""

    DEFAULT_CSS = """
    CardWidget {
        border: solid $primary;
        background: $surface-darken-1;
        padding: 1 2;
        width: 100%;
        height: auto;
        min-height: 6;
    }

    CardWidget:hover {
        border: solid $accent;
        background: $surface;
    }

    CardWidget.selected {
        border: double $accent;
        background: $primary-darken-1;
    }

    .card-name {
        color: $text;
        text-style: bold;
    }

    .card-arcana {
        color: $secondary;
    }

    .card-suit {
        color: $text-muted;
    }

    .card-orientation {
        color: $accent;
    }

    .card-position {
        color: $primary;
        text-style: italic;
    }
    """

    def __init__(
        self, card_position: CardPosition | None = None, index: int = 0, **kwargs: Any
    ) -> None:
        """Initialize the card widget."""
        super().__init__(**kwargs)
        self.card_position = card_position
        self.card_index = index
        self.is_selected = False

    def compose(self) -> ComposeResult:
        """Compose the card widget."""
        if self.card_position is None:
            yield Static("[Empty]", classes="card-name")
            return

        card = self.card_position.card

        yield Static(card.name, classes="card-name")
        yield Static(f"{card.arcana.value.title()} Arcana", classes="card-arcana")

        if card.suit:
            yield Static(
                f"{card.suit.symbol} {card.suit.full_name}", classes="card-suit"
            )

        show_reversed = getattr(self.app, "show_reversed", False)
        if not show_reversed:
            orientation = "↑ Upright"
        else:
            orientation = "↓ Reversed" if not card.upright else "↑ Upright"
        yield Static(orientation, classes="card-orientation")

        yield Static(
            f"Position: {self.card_position.position_label}", classes="card-position"
        )

    def update_card(self, card_position: CardPosition) -> None:
        """Update the card displayed in this widget."""
        self.card_position = card_position
        self.refresh()

    def toggle_selection(self) -> None:
        """Toggle the selected state of this card."""
        self.is_selected = not self.is_selected
        self.set_class(self.is_selected, "selected")

    def select(self) -> None:
        """Select this card."""
        self.is_selected = True
        self.set_class(True, "selected")

    def deselect(self) -> None:
        """Deselect this card."""
        self.is_selected = False
        self.set_class(False, "selected")

    def on_click(self, event: events.Click) -> None:
        """Handle click events."""
        if self.card_position:
            action = getattr(self.app, "action_show_card_detail", None)
            if action:
                action(self.card_position, self.card_index)
