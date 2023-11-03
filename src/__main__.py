import os
# The following environment variable must be set before importing moviepy, 
# otherwise moviepy won't be able to find ffmpeg when the app is compiled
# and it will crash on startup.
os.environ["IMAGEIO_FFMPEG_EXE"] = "src\\imageio_ffmpeg\\ffmpeg-win64-v4.2.2.exe"

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
