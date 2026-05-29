"""Spread layout widget for the TUI."""

from typing import Any

from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static

from orbpondering.models import CardPosition

from .card_widget import CardWidget


class SpreadLayout(Container):
    """Widget to display a tarot spread layout."""

    DEFAULT_CSS = """
    SpreadLayout {
        border: solid $accent;
        background: $surface;
        padding: 1;
        height: 1fr;
    }

    SpreadLayout .spread-empty {
        color: $text-muted;
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("n", "next_card", "Next Card"),
        ("p", "prev_card", "Prev Card"),
        ("r", "reveal_card", "Reveal Card"),
    ]

    def __init__(
        self, positions: list[CardPosition] | None = None, **kwargs: Any
    ) -> None:
        """Initialize the spread layout."""
        super().__init__(**kwargs)
        self.positions = positions or []
        self.card_widgets: list[CardWidget] = []
        self.selected_index: int = 0

    def compose(self) -> ComposeResult:
        """Compose the spread layout."""
        yield from self._build_content()

    def _build_content(self) -> ComposeResult:
        """Build the widget content based on positions."""
        if not self.positions:
            yield Static(
                "No cards drawn yet. Press Calculate to start a reading.",
                classes="spread-empty",
            )
            return

        for idx, pos in enumerate(self.positions):
            card_widget = CardWidget(pos, index=idx)
            self.card_widgets.append(card_widget)
            yield card_widget

        if self.card_widgets:
            self.card_widgets[0].select()

    def populate(self, positions: list[CardPosition]) -> None:
        """Populate the spread with card positions."""
        self.positions = positions
        self.card_widgets.clear()
        self.selected_index = 0

        for child in list(self.children):
            child.remove()

        for idx, pos in enumerate(positions):
            card_widget = CardWidget(pos, index=idx)
            self.card_widgets.append(card_widget)
            self.mount(card_widget)

        if self.card_widgets:
            self.card_widgets[0].select()

        self.refresh()

    def action_next_card(self) -> None:
        """Select the next card in the spread."""
        if not self.card_widgets:
            return

        self.card_widgets[self.selected_index].deselect()
        self.selected_index = (self.selected_index + 1) % len(self.card_widgets)
        self.card_widgets[self.selected_index].select()

    def action_prev_card(self) -> None:
        """Select the previous card in the spread."""
        if not self.card_widgets:
            return

        self.card_widgets[self.selected_index].deselect()
        self.selected_index = (self.selected_index - 1) % len(self.card_widgets)
        self.card_widgets[self.selected_index].select()

    def action_reveal_card(self) -> None:
        """Reveal the currently selected card."""
        if self.card_widgets and self.selected_index < len(self.card_widgets):
            card = self.card_widgets[self.selected_index].card_position
            action = getattr(self.app, "action_show_card_detail", None)
            if action:
                action(card, self.selected_index)
