"""Orbpondering native client app."""

import toga

from .screens.settings import SettingsScreen


class OrbponderingClient(toga.App):
    """Orbpondering native client application."""

    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name, size=(400, 600))
        self.main_window.content = SettingsScreen(self)
        self.main_window.show()


def main():
    return OrbponderingClient("Orbpondering", "net.phildini.orbpondering")
