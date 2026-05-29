"""Settings screen implementation for the TUI."""

from datetime import date, datetime
from typing import Any

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label

from orbpondering.constants import HouseSystem
from orbpondering.models import BirthData


class SettingsScreen(Screen):
    """Settings screen."""

    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("tab", "next_field", "Next Field"),
        ("shift+tab", "prev_field", "Prev Field"),
        ("enter", "calculate", "Calculate"),
    ]

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the settings screen."""
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        """Compose the settings screen layout."""
        yield Container(
            Label("[b]SETTINGS[/b]", id="settings-title"),
            Vertical(
                Label("[b]Date/Time[/b]", classes="section-header"),
                Horizontal(
                    Label("Date (YYYY-MM-DD):"),
                    Input(value=date.today().isoformat(), placeholder="YYYY-MM-DD", id="date-input"),
                ),
                Horizontal(
                    Label("Time (HH:MM):"),
                    Input(value="12:00", placeholder="HH:MM", id="time-input"),
                ),
                Label("[b]Location[/b]", classes="section-header"),
                Horizontal(
                    Label("Latitude:"),
                    Input(value="0.0", placeholder="-90 to 90", id="lat-input"),
                ),
                Horizontal(
                    Label("Longitude:"),
                    Input(value="0.0", placeholder="-180 to 180", id="lon-input"),
                ),
                Label("[b]Astrology[/b]", classes="section-header"),
                Horizontal(
                    Label("House System:"),
                    Input(value="whole_sign", placeholder="whole_sign", id="house-input"),
                ),
                Horizontal(
                    Label("Spread Type:"),
                    Input(value="daily", placeholder="daily, three_card, celtic_cross", id="spread-input"),
                ),
                Horizontal(
                    Label("Reversed Cards:"),
                    Input(value="no", placeholder="yes/no", id="reversed-input"),
                ),
                Label("[b]Natal Chart (Optional)[/b]", classes="section-header"),
                Horizontal(
                    Label("Enable Natal:"),
                    Input(value="no", placeholder="yes/no", id="natal-enable-input"),
                ),
                Horizontal(
                    Label("Birth Date:"),
                    Input(value="", placeholder="YYYY-MM-DD", id="birth-date-input"),
                ),
                Horizontal(
                    Label("Birth Time:"),
                    Input(value="", placeholder="HH:MM", id="birth-time-input"),
                ),
                Horizontal(
                    Label("Birth Lat:"),
                    Input(value="0.0", placeholder="-90 to 90", id="birth-lat-input"),
                ),
                Horizontal(
                    Label("Birth Lon:"),
                    Input(value="0.0", placeholder="-180 to 180", id="birth-lon-input"),
                ),
                id="settings-form",
            ),
            Container(
                Button("Calculate", id="calculate-button", variant="primary"),
                Button("Cancel", id="cancel-button"),
                id="settings-buttons",
            ),
            id="settings-screen",
        )

    def on_mount(self) -> None:
        """Called when screen is mounted."""
        date_input = self.query_one("#date-input", Input)
        date_input.focus()

    def action_go_back(self) -> None:
        """Go back to the main screen."""
        self.app.pop_screen()

    def action_next_field(self) -> None:
        """Move to next input field."""
        inputs = [
            "#date-input",
            "#time-input",
            "#lat-input",
            "#lon-input",
            "#house-input",
            "#spread-input",
            "#reversed-input",
            "#natal-enable-input",
            "#birth-date-input",
            "#birth-time-input",
            "#birth-lat-input",
            "#birth-lon-input",
        ]
        focused = self.app.screen.query_one(":focus", Input)
        if focused:
            current_id = focused.id
            if current_id in inputs:
                current_index = inputs.index(current_id)
                next_index = (current_index + 1) % len(inputs)
                next_input = self.query_one(inputs[next_index], Input)
                next_input.focus()

    def action_prev_field(self) -> None:
        """Move to previous input field."""
        inputs = [
            "#date-input",
            "#time-input",
            "#lat-input",
            "#lon-input",
            "#house-input",
            "#spread-input",
            "#reversed-input",
            "#natal-enable-input",
            "#birth-date-input",
            "#birth-time-input",
            "#birth-lat-input",
            "#birth-lon-input",
        ]
        focused = self.app.screen.query_one(":focus", Input)
        if focused:
            current_id = focused.id
            if current_id in inputs:
                current_index = inputs.index(current_id)
                prev_index = (current_index - 1) % len(inputs)
                prev_input = self.query_one(inputs[prev_index], Input)
                prev_input.focus()

    def action_calculate(self) -> None:
        """Calculate reading."""
        self._calculate_reading()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "cancel-button":
            self.action_go_back()
        elif event.button.id == "calculate-button":
            self._calculate_reading()

    def _calculate_reading(self) -> None:
        """Parse inputs and calculate a reading."""
        date_input = self.query_one("#date-input", Input).value
        time_input = self.query_one("#time-input", Input).value
        lat_input = self.query_one("#lat-input", Input).value
        lon_input = self.query_one("#lon-input", Input).value
        house_input = self.query_one("#house-input", Input).value
        spread_input = self.query_one("#spread-input", Input).value
        reversed_input = self.query_one("#reversed-input", Input).value.lower()
        natal_enable = self.query_one("#natal-enable-input", Input).value.lower() == "yes"

        birth_date_input = self.query_one("#birth-date-input", Input).value
        birth_time_input = self.query_one("#birth-time-input", Input).value
        birth_lat_input = self.query_one("#birth-lat-input", Input).value
        birth_lon_input = self.query_one("#birth-lon-input", Input).value

        try:
            reading_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        except ValueError:
            reading_date = date.today()

        try:
            datetime.strptime(time_input, "%H:%M")
        except ValueError:
            pass

        try:
            lat = float(lat_input) if lat_input else 0.0
        except ValueError:
            lat = 0.0

        try:
            lon = float(lon_input) if lon_input else 0.0
        except ValueError:
            lon = 0.0

        house_str = house_input.strip().lower() if house_input else "whole_sign"
        try:
            house_system = HouseSystem(house_str)
        except ValueError:
            house_system = HouseSystem.WHOLE_SIGN

        spread_name = spread_input.strip() if spread_input else "daily"
        reversed_cards = reversed_input == "yes"

        setattr(self.app, "show_reversed", reversed_cards)

        if natal_enable and birth_date_input:
            try:
                b_date = datetime.strptime(birth_date_input, "%Y-%m-%d").date()
            except ValueError:
                b_date = None

            b_time = None
            if birth_time_input:
                try:
                    b_time = datetime.strptime(birth_time_input, "%H:%M").time()
                except ValueError:
                    pass

            try:
                b_lat = float(birth_lat_input) if birth_lat_input else 0.0
            except ValueError:
                b_lat = 0.0

            try:
                b_lon = float(birth_lon_input) if birth_lon_input else 0.0
            except ValueError:
                b_lon = 0.0

            if b_date:
                birth_data = BirthData(date=b_date, time=b_time, lat=b_lat, lon=b_lon, tz=None)

                from orbpondering.draw import birth_tarot_draw

                reading = birth_tarot_draw(
                    d=reading_date,
                    lat=lat,
                    lon=lon,
                    birth_data=birth_data,
                    house_system=house_system,
                    spread_name=spread_name,
                    reversed_cards=reversed_cards,
                )
            else:
                from orbpondering.draw import tarot_draw_for_date

                reading = tarot_draw_for_date(
                    d=reading_date,
                    lat=lat,
                    lon=lon,
                    house_system=house_system,
                    spread_name=spread_name,
                    reversed_cards=reversed_cards,
                )
        else:
            from orbpondering.draw import tarot_draw_for_date

            reading = tarot_draw_for_date(
                d=reading_date,
                lat=lat,
                lon=lon,
                house_system=house_system,
                spread_name=spread_name,
                reversed_cards=reversed_cards,
            )

        setattr(self.app, "reading", reading)
        setattr(self.app, "_pending_reading_update", True)
        self.action_go_back()
