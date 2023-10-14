from PySide6.QtCore import Slot

from ..line_edit_base import LineEditBase
from settings.settings import Settings


class StartStopRecordingLineEdit(LineEditBase):

    HOTKEY_NAME = "start_stop_recording"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_hotkey_from_settings(self.HOTKEY_NAME)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.stopped_listening_for_key_combos_signal.connect(
            self.on_stopped_listening_for_key_combos
        )

    def load_hotkey_from_settings(self, hotkey_name):
        self.setText(Settings.get_hotkeys()[hotkey_name])

    @Slot()
    def on_stopped_listening_for_key_combos(self, combo_string):
        Settings.set_hotkey(self.HOTKEY_NAME, combo_string)
