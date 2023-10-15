from PySide6.QtCore import Slot

from ..line_edit_base import LineEditBase
from settings.settings import Settings


class StartStopRecordingLineEdit(LineEditBase):

    __HOTKEY_NAME = "start_stop_recording"
    __NONE_TEXT = "None"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_hotkey_from_settings(self.__HOTKEY_NAME)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.key_combo_listener.listener_started_signal.connect(
            self.on_key_combo_listener_started
        )
        self.key_combo_listener.combo_valid_signal.connect(
            self.on_key_combo_valid
        )
        self.key_combo_listener.combo_in_use_signal.connect(
            self.on_key_combo_in_use
        )

    def load_hotkey_from_settings(self, hotkey_name):
        hotkey = Settings.get_hotkeys()[hotkey_name]
        if hotkey == "":
            self.setText(self.__NONE_TEXT)
        else:
            self.setText(hotkey)
    
    @Slot()
    def on_key_combo_listener_started(self):
        Settings.set_hotkey(self.__HOTKEY_NAME, "")

    @Slot()
    def on_key_combo_valid(self, combo_string):
        Settings.set_hotkey(self.__HOTKEY_NAME, combo_string)

    @Slot()
    def on_key_combo_in_use(self):
        Settings.set_hotkey(self.__HOTKEY_NAME, "")
