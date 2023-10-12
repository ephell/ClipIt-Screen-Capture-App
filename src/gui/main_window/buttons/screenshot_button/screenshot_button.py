import datetime

import mss
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton

from gui.main_window.buttons.recording_area_selector._area_selector import AreaSelector
from settings.settings import Settings


class ScreenshotButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.area_selector = None

    @Slot()
    def on_screenshot_button_clicked(self):
        self.area_selector = AreaSelector(self.__take_screenshot, self)
        self.area_selector.show()
        
    def __take_screenshot(self, x0, y0, x1, y1):
        """Callback function for the area selector."""
        # Calling close() early prevents the drawn dotted lines around
        # the selected area from being captured.
        if self.area_selector is not None:
            self.area_selector.close()
        with mss.mss() as sct:
            sc = sct.grab({
                'top': int(y0),
                'left': int(x0),
                'width': int(x1 - x0),
                'height': int(y1 - y0)
            })
        mss.tools.to_png(sc.rgb, sc.size, output=self.__generate_file_path())

    def __generate_file_path(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        return f"{Settings.get_capture_dir_path()}/{timestamp}.png"
