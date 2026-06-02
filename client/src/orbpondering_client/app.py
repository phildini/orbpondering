"""Orbpondering native client app."""

import toga

from .screens.settings import SettingsScreen


class OrbponderingClient(toga.App):
    """Orbpondering native client application."""

    def startup(self):
        self.reading = None
        self.main_window = toga.MainWindow(title=self.formal_name, size=(400, 700))
        self.main_window.content = SettingsScreen(self)
        self.main_window.show()

    def open_reading(self, reading_data: dict) -> None:
        """Show the reading results screen."""
        from .screens.reading import ReadingScreen

        self.reading = reading_data
        self.main_window.content = ReadingScreen(self)

    def open_chart(self) -> None:
        """Show the planetary chart screen."""
        from .screens.chart import ChartScreen

        self.main_window.content = ChartScreen(self)

    def open_glossary(self) -> None:
        """Show the planet glossary screen."""
        from .screens.glossary import GlossaryScreen

        self.main_window.content = GlossaryScreen(self)

    def back_to_settings(self) -> None:
        """Return to the settings screen."""
        self.main_window.content = SettingsScreen(self)


def main():
    return OrbponderingClient("Orbpondering", "net.phildini.orbpondering")
