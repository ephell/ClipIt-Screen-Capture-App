from PySide6.QtCore import Slot, Signal

from ..line_edit_base import LineEditBase
from settings.settings import Settings


class ScreenshotLineEdit(LineEditBase):

    HOTKEY_NAME = "screenshot"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_hotkey_from_settings(self.HOTKEY_NAME)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.key_combo_listener_stopped_signal.connect(
            self.on_key_combo_listener_stopped
        )

    def load_hotkey_from_settings(self, hotkey_name):
        self.setText(Settings.get_hotkeys()[hotkey_name])
    
    @Slot()
    def on_key_combo_listener_stopped(self, combo_string):
        Settings.set_hotkey(self.HOTKEY_NAME, combo_string)
