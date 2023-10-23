import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

from settings.settings import Settings


class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.__create_directories()
        self.setStyle("Fusion")
        self.setPalette(self.__get_default_palette(self))

    def __create_directories(self):
        """Creates directories for temporary files and final output."""
        if not os.path.exists(Settings.get_capture_dir_path()):
            Settings.set_capture_dir_path(os.path.join(os.getcwd(), "captures"))
            if not os.path.exists(Settings.get_capture_dir_path()):
                os.makedirs(Settings.get_capture_dir_path())
        if not os.path.exists(Settings.get_temp_dir_path()):
            os.makedirs(Settings.get_temp_dir_path())

    def __get_default_palette(self, application: QApplication):
        palette = application.palette()
        palette.setColorGroup(
            QPalette.Active,     # color group
            Qt.white,            # windowText
            QColor(65, 65, 65),  # button
            QColor(95, 95, 95),  # light
            QColor(40, 40, 40),  # dark
            QColor(60, 60, 60),  # mid
            Qt.white,            # text
            Qt.blue,             # bright_text
            QColor(55, 55, 55),  # base
            QColor(40, 40, 40)   # window
        )
        palette.setColorGroup(
            QPalette.Inactive,   # color group
            Qt.white,            # windowText
            QColor(65, 65, 65),  # button
            QColor(95, 95, 95),  # light
            QColor(40, 40, 40),  # dark
            QColor(60, 60, 60),  # mid
            Qt.white,            # text
            Qt.blue,             # bright_text
            QColor(55, 55, 55),  # base
            QColor(40, 40, 40)   # window
        )
        return palette
