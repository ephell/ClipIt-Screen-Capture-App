from PySide6.QtWidgets import QPushButton

from .settings_window.settings_window import SettingsWindow


class SettingsButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)

    def on_settings_button_clicked(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

