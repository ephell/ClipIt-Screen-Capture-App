from PySide6.QtCore import Slot
from PySide6.QtWidgets import QCheckBox

from settings.settings import Settings


class RecordMicrophoneAudioCheckBox(QCheckBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setChecked(self.__get_checked_state_from_settings())
        self.stateChanged.connect(self.__update_settings)

    def __get_checked_state_from_settings(self):
        return Settings.get_audio_preferences().getboolean("RECORD_MICROPHONE")
    
    @Slot()
    def __update_settings(self, state):
        Settings.set_audio_preference("RECORD_MICROPHONE", str(bool(state)))
