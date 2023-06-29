import os
import sys

from PySide6.QtWidgets import QApplication

from gui.main_window.main_window import MainWindow
from settings import Paths


def __create_directories():
    """Creates directories for temporary files and final output."""
    if not os.path.exists(Paths.TEMP_DIR):
        os.makedirs(Paths.TEMP_DIR)
    if not os.path.exists(Paths.RECORDINGS_DIR):
        os.makedirs(Paths.RECORDINGS_DIR)

    
if __name__ == "__main__":
    __create_directories()
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
