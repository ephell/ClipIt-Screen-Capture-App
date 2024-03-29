from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget

from .SettingsWindow_ui import Ui_SettingsWindow


class SettingsWindow(QWidget, Ui_SettingsWindow):

    left_mouse_button_pressed_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("ClipIt - Settings")
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.browse_button.new_directory_selected_signal.connect(
            self.captures_dir_line_edit.on_new_directory_selected
        )
        self.left_mouse_button_pressed_signal.connect(
            self.screenshot_line_edit.on_left_mouse_button_pressed_on_settings_window
        )
        self.left_mouse_button_pressed_signal.connect(
            self.start_stop_recording_line_edit.on_left_mouse_button_pressed_on_settings_window
        )
        self.screenshot_line_edit.focus_in_event_signal.connect(
            self.screenshot_status_label.on_screenshot_line_edit_focus_in_event
        )
        self.screenshot_line_edit.focus_out_event_signal.connect(
            self.screenshot_status_label.on_screenshot_line_edit_focus_out_event
        )
        self.start_stop_recording_line_edit.focus_in_event_signal.connect(
            self.start_stop_recording_status_label.on_screenshot_line_edit_focus_in_event
        )
        self.start_stop_recording_line_edit.focus_out_event_signal.connect(
            self.start_stop_recording_status_label.on_screenshot_line_edit_focus_out_event
        )

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.left_mouse_button_pressed_signal.emit()
