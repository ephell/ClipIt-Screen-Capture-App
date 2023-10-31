from multiprocessing import freeze_support
import sys

from src.gui.application.application import Application
from src.gui.main_window.main_window import MainWindow

    
if __name__ == "__main__":
    freeze_support()
    app = Application(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()