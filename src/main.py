import os
import sys

from PySide6.QtWidgets import QApplication

from gui.main_window.main_window import MainWindow
from settings.settings import Settings


def __create_directories():
    """Creates directories for temporary files and final output."""
    if not os.path.exists(Settings.get_capture_dir_path()):
        os.makedirs(Settings.get_capture_dir_path())
    if not os.path.exists(Settings.get_temp_dir_path()):
        os.makedirs(Settings.get_temp_dir_path())

    
if __name__ == "__main__":
    __create_directories()
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
