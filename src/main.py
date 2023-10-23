import sys

from gui.application.application import Application
from gui.main_window.main_window import MainWindow

    
if __name__ == "__main__":
    app = Application(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()
