import os

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton

from src.settings.settings import Settings


class OpenCaptureFolderButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def on_open_capture_folder_button_clicked(self):
        os.startfile(Settings.get_capture_dir_path())
