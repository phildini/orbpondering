"""Settings screen with input form."""

from datetime import date

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

ELEMENT_COLORS = {
    "fire": "#e74c3c",
    "water": "#3498db",
    "air": "#f39c12",
    "earth": "#27ae60",
}


class SettingsScreen(toga.Box):
    """Form for entering astrological parameters."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN, padding=20))
        self._app = app

        today = date.today()
        self._build_form(today)

    def _build_form(self, today: date) -> None:
        scroll = toga.ScrollContainer(style=Pack(flex=1))
        form = toga.Box(style=Pack(direction=COLUMN, padding=5))

        # --- Date ---
        form.add(toga.Label("Date", style=Pack(padding=(0, 0, 2, 0))))
        self.date_input = toga.DateInput(
            value=today,
            style=Pack(padding=(0, 0, 12, 0)),
        )
        form.add(self.date_input)

        # --- Location ---
        form.add(
            toga.Label("Location", style=Pack(font_weight="bold", padding=(0, 0, 4, 0)))
        )
        loc_row = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 4, 0)))
        self.lat_input = toga.NumberInput(
            value=0.0,
            step=0.0001,
            style=Pack(flex=1, padding=(0, 4, 0, 0)),
        )
        self.lon_input = toga.NumberInput(
            value=0.0,
            step=0.0001,
            style=Pack(flex=1),
        )
        loc_row.add(
            toga.Label("Lat", style=Pack(width=30, padding=(0, 4, 0, 0))),
            self.lat_input,
            toga.Label("Lon", style=Pack(width=30, padding=(0, 4, 0, 0))),
            self.lon_input,
        )
        form.add(loc_row)

        self.locate_btn = toga.Button(
            "📍 Use My Location",
            on_press=self._on_locate,
            style=Pack(padding=(0, 0, 4, 0)),
        )
        form.add(self.locate_btn)
        self.location_status = toga.Label(
            "",
            style=Pack(padding=(0, 0, 12, 0), font_size=11),
        )
        form.add(self.location_status)

        # --- House System ---
        form.add(
            toga.Label("House System", style=Pack(padding=(0, 0, 2, 0)))
        )
        self.house_select = toga.Selection(
            items=["whole_sign", "equal", "porphyry", "placidus"],
            style=Pack(padding=(0, 0, 12, 0)),
        )
        form.add(self.house_select)

        # --- Spread ---
        form.add(toga.Label("Spread", style=Pack(padding=(0, 0, 2, 0))))
        self.spread_select = toga.Selection(
            items=["daily", "three_card", "celtic_cross"],
            style=Pack(padding=(0, 0, 12, 0)),
        )
        form.add(self.spread_select)

        # --- Reversed ---
        self.reversed_switch = toga.Switch(
            "Allow reversed cards",
            style=Pack(padding=(0, 0, 12, 0)),
        )
        form.add(self.reversed_switch)

        # --- Natal mode toggle ---
        self.natal_switch = toga.Switch(
            "Natal chart mode",
            on_change=self._on_natal_toggle,
            style=Pack(padding=(0, 0, 4, 0)),
        )
        form.add(self.natal_switch)

        # --- Natal fields (initially hidden) ---
        self._natal_box = self._build_natal_fields(today)
        self._natal_visible = False

        # --- Calculate ---
        self.calc_btn = toga.Button(
            "✦  Calculate Reading",
            on_press=self._on_calculate,
            style=Pack(padding=(12, 0, 4, 0)),
        )
        form.add(self.calc_btn)

        self.activity = toga.ActivityIndicator(
            style=Pack(padding=(8, 0, 0, 0)),
        )
        form.add(self.activity)

        self.error_label = toga.Label(
            "",
            style=Pack(padding=(4, 0, 0, 0), font_size=11, color="#e74c3c"),
        )
        form.add(self.error_label)

        scroll.content = form
        self.add(scroll)

    def _build_natal_fields(self, today: date) -> toga.Box:
        box = toga.Box(style=Pack(direction=COLUMN, padding=(8, 0, 0, 0)))

        box.add(
            toga.Label(
                "Natal Chart",
                style=Pack(font_weight="bold", font_size=13, padding=(0, 0, 4, 0)),
            )
        )

        box.add(toga.Label("Birth Date", style=Pack(padding=(0, 0, 2, 0))))
        self.birth_date_input = toga.DateInput(
            value=today,
            style=Pack(padding=(0, 0, 8, 0)),
        )
        box.add(self.birth_date_input)

        box.add(toga.Label("Birth Time", style=Pack(padding=(0, 0, 2, 0))))
        self.birth_time_input = toga.TimeInput(
            style=Pack(padding=(0, 0, 8, 0)),
        )
        box.add(self.birth_time_input)

        box.add(toga.Label("Birth Location", style=Pack(padding=(0, 0, 2, 0))))
        birth_loc = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 4, 0)))
        self.birth_lat = toga.NumberInput(value=0.0, step=0.0001, style=Pack(flex=1, padding=(0, 4, 0, 0)))
        self.birth_lon = toga.NumberInput(value=0.0, step=0.0001, style=Pack(flex=1))
        birth_loc.add(
            toga.Label("Lat", style=Pack(width=30, padding=(0, 4, 0, 0))),
            self.birth_lat,
            toga.Label("Lon", style=Pack(width=30, padding=(0, 4, 0, 0))),
            self.birth_lon,
        )
        box.add(birth_loc)

        box.add(toga.Label("Time Zone", style=Pack(padding=(0, 0, 2, 0))))
        self.birth_tz = toga.TextInput(
            placeholder="America/New_York",
            style=Pack(padding=(0, 0, 8, 0)),
        )
        box.add(self.birth_tz)

        return box

    def _on_natal_toggle(self, widget: toga.Switch) -> None:
        if widget.value and not self._natal_visible:
            self._natal_visible = True
            self.parent.insert(self.parent.indexOf(self.natal_switch) + 1, self._natal_box)
        elif not widget.value and self._natal_visible:
            self._natal_visible = False
            if self._natal_box.parent:
                self._natal_box.parent.remove(self._natal_box)

    def _on_locate(self, widget: toga.Button) -> None:
        location = self._app.location
        if not location.has_permission():
            location.request_permission()

        try:
            pos = location.current_location
            self.lat_input.value = pos.latitude
            self.lon_input.value = pos.longitude
            self.location_status.text = f"📍 {pos.latitude:.2f}, {pos.longitude:.2f}"
            self.location_status.style.color = "#27ae60"
        except Exception as e:
            self.location_status.text = f"Location unavailable: {e}"
            self.location_status.style.color = "#e74c3c"

    def _on_calculate(self, widget: toga.Button) -> None:
        self.error_label.text = ""
        self.activity.start()
        self.calc_btn.enabled = False

        try:
            reading = self._do_calculate()
            self.activity.stop()
            self._app.open_reading(reading)
        except Exception as e:
            self.activity.stop()
            self.calc_btn.enabled = True
            self.error_label.text = str(e)

    def _do_calculate(self) -> dict:
        date_val = self.date_input.value.isoformat() if self.date_input.value else None
        lat = self.lat_input.value or 0.0
        lon = self.lon_input.value or 0.0
        house = self.house_select.value or "whole_sign"
        spread = self.spread_select.value or "daily"
        reversed = self.reversed_switch.value

        if self.natal_switch.value:
            from ..api import create_natal_reading

            return create_natal_reading(
                date=date_val,
                lat=lat,
                lon=lon,
                house_system=house,
                spread=spread,
                reversed=reversed,
                birth_date=self.birth_date_input.value.isoformat(),
                birth_time=self.birth_time_input.value.strftime("%H:%M"),
                birth_lat=self.birth_lat.value or 0.0,
                birth_lon=self.birth_lon.value or 0.0,
                birth_tz=self.birth_tz.value or None,
            )
        else:
            from ..api import create_reading

            return create_reading(
                date=date_val,
                lat=lat,
                lon=lon,
                house_system=house,
                spread=spread,
                reversed=reversed,
            )
