import ctypes
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtCore import Qt

from settings.settings import Settings


class Application(QApplication):

    __ICON_PATH = "src/gui/application/logo.svg"
    __STYLE = "Fusion"
    __CAPTURES_DIR_NAME = "captures"

    def __init__(self, argv):
        super().__init__(argv)
        self.setWindowIcon(QIcon(self.__ICON_PATH))
        self.setQuitOnLastWindowClosed(False)
        self.__set_app_id()
        self.__create_directories()
        self.setStyle(self.__STYLE)
        self.setPalette(self.__get_default_palette(self))

    def __set_app_id(self):
        """
        Set AppUserModelID so that the app icon is displayed in the taskbar.
        
        https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
        """
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ClipIt.Application")

    def __create_directories(self):
        """Creates directories for temporary files and final output."""
        if not os.path.exists(Settings.get_capture_dir_path()):
            Settings.set_capture_dir_path(os.path.join(os.getcwd(), self.__CAPTURES_DIR_NAME))
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
