from PySide6.QtCore import Slot

from ..status_label_base import StatusLabelBase
from src.settings.settings import Settings


class ScreenshotStatusLabel(StatusLabelBase):

    __HOTKEY_NAME = "screenshot"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.set_initial_state()

    def set_initial_state(self):
        if Settings.get_hotkeys()[self.__HOTKEY_NAME] != "":
            self.set_state_normal()
        else:
            self.set_state_error()

    @Slot()
    def on_screenshot_line_edit_focus_in_event(self):
        self.set_state_pending()

    @Slot()
    def on_screenshot_line_edit_focus_out_event(self, line_edit_text):
        if Settings.get_hotkeys()[self.__HOTKEY_NAME] == line_edit_text:
            self.set_state_normal()
        else:
            self.set_state_error()
