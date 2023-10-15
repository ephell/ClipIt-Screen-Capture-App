from PySide6.QtCore import Slot
from PySide6.QtWidgets import QLineEdit

from settings.settings import Settings


class CapturesDirectoryLineEdit(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__load_current_capture_dir_path()
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.textChanged.connect(self.__on_text_changed)

    def __load_current_capture_dir_path(self):
        self.setText(Settings.get_capture_dir_path())

    @Slot()
    def on_new_directory_selected(self, directory_path):
        self.setText(directory_path)

    @Slot()
    def __on_text_changed(self):
        Settings.set_capture_dir_path(self.text())
