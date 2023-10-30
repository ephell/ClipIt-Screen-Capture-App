import datetime

from io import BytesIO
import mss
from playsound import playsound
from PIL import Image
from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QImage
import win32clipboard

from gui.area_widgets.area_selector import AreaSelector
from gui.notification_sender.notification_sender import NotificationSender
from src.settings.settings import Settings


class ScreenshotButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.area_selector = None
        self.__notification_sender = NotificationSender()

    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.area_selector is not None:
                try:
                    self.area_selector.close()
                except RuntimeError:
                    # Catches 'Internal C++ object (AreaSelector) already deleted'.
                    # Not a good solution, but passing is not a problem here.
                    pass 

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
        playsound("src/gui/main_window/buttons/screenshot_button/camera-click.wav")
        file_path = self.__generate_file_path()
        mss.tools.to_png(sc.rgb, sc.size, output=file_path)
        self.__send_to_clipboard(file_path)
        self.__notification_sender.send(
            f"Screenshot saved to: {file_path}",
            3000,
            QImage(file_path)
        )

    def __generate_file_path(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        return f"{Settings.get_capture_dir_path()}/{timestamp}.png"

    def __send_to_clipboard(self, screenshot_path):
        screenshot = Image.open(screenshot_path)
        output = BytesIO()
        screenshot.convert("RGB").save(output, "DIB")
        data = output.getvalue()
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()

    @Slot()
    def on_screenshot_button_clicked(self):
        self.area_selector = AreaSelector(self.__take_screenshot, self)
        self.area_selector.show()

    @Slot()
    def on_hotkey_pressed(self):
        self.on_screenshot_button_clicked()
