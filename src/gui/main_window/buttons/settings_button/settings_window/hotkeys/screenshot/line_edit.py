from PySide6.QtCore import Slot

from ..line_edit_base import LineEditBase
from settings.settings import Settings


class ScreenshotLineEdit(LineEditBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.stopped_listening_for_key_combos_signal.connect(
            self.on_stopped_listening_for_key_combos
        )

    @Slot()
    def on_stopped_listening_for_key_combos(self, combo_string):
        Settings.set_hotkey("screenshot", combo_string)
