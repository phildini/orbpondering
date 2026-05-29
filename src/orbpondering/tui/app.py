"""Main TUI application class with screen routing."""

from typing import TYPE_CHECKING, Any

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header

if TYPE_CHECKING:
    from orbpondering.models import TarotReading


class TUIApp(App):
    """Main TUI application class with screen routing."""

    CSS_PATH = "app.css"

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f1", "help", "Help"),
        ("f2", "settings", "Settings"),
        ("f5", "save_reading", "Save"),
    ]

    def __init__(self) -> None:
        """Initialize the TUI application."""
        super().__init__()
        self.reading: TarotReading | None = None
        self.show_reversed: bool = False

    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        yield Container(id="main-container")
        yield Footer()

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        from .screens.main import MainScreen
        from .widgets.status_bar import StatusBar

        container = self.query_one("#main-container")
        container.mount(StatusBar())
        self.push_screen(MainScreen())

    async def action_quit(self) -> None:
        """Quit the application."""
        self.exit()

    def action_help(self) -> None:
        """Show help information."""
        self.notify(
            "F1:Help F2:Settings F3:Spread F4:Chart F5:Save H:History Q:Quit"
        )

    def action_settings(self) -> None:
        """Open settings screen."""
        from .screens.settings import SettingsScreen

        self.push_screen(SettingsScreen())

    def action_save_reading(self) -> None:
        """Save the current reading."""
        reading = getattr(self, "reading", None)
        if reading is None:
            self.notify("No reading to save. Calculate a reading first.")
            return

        from orbpondering.service import save_reading

        try:
            save_reading(reading)
            self.notify("Reading saved successfully!")
        except Exception as e:
            self.notify(f"Failed to save reading: {e}")

    def action_show_card_detail(self, card_position: Any, index: int) -> None:
        """Show card detail modal."""
        from .screens.card_detail import CardDetailView

        reading = getattr(self, "reading", None)
        total = len(reading.positions) if reading and reading.positions else 1
        self.push_screen(CardDetailView(card_position, index, total))
