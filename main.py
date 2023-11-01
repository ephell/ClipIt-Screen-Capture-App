from multiprocessing import freeze_support
import sys
from time import sleep

from src.gui.application.application import Application
from src.gui.main_window.main_window import MainWindow
from src.utilities.console_hider import ConsoleHider
from src.utilities.single_instance_checker import SingleInstanceChecker


def main():
    freeze_support()
    instance_checker = SingleInstanceChecker()
    if instance_checker.is_another_instance_already_running():
        print(
            "Another instance of ClipIt is already running!\n"
            "Closing this instance in 3 seconds..."
        )
        sleep(3)
        sys.exit(0)
    console_hider = ConsoleHider()
    console_hider.start()
    app = Application(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
