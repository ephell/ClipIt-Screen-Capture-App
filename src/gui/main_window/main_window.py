from logger import GlobalLogger
log = GlobalLogger.LOGGER

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow

from .Ui_MainWindow import Ui_MainWindow
from .buttons.settings_button.settings_window.hotkeys.hotkey_listener import HotkeyListener
from gui.main_window.buttons.debug_button.debug_button import DebugButton


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.__set_stylesheet("src/gui/main_window/MainWindow.qss")
        self.app = app
        self.first_window_resize_event = True
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.start()
        self.__connect_signals_and_slots()
        # Debug button for various prints to console (not in MainWindow.ui)
        # self.debug_button = DebugButton(self)
        # self.central_layout.addWidget(self.debug_button)
        # self.debug_button.clicked.connect(self.debug_button.on_debug_button_clicked)

    def __connect_signals_and_slots(self):
        self.record_button.clicked.connect(
            self.record_button.on_record_button_clicked
        )
        self.record_button.open_editor_after_file_generation_finished_signal.connect(
            self.open_editor_button.on_file_generation_finished
        )
        self.open_editor_button.clicked.connect(
            self.open_editor_button.on_open_editor_button_clicked
        )
        self.open_capture_folder_button.clicked.connect(
            self.open_capture_folder_button.on_open_capture_folder_button_clicked
        )
        self.screenshot_button.clicked.connect(
            self.screenshot_button.on_screenshot_button_clicked
        )
        self.settings_button.clicked.connect(
            self.settings_button.on_settings_button_clicked
        )
        self.hotkey_listener.hotkey_detected_signal.connect(
            self.__on_hotkey_detected
        )

    def __set_stylesheet(self, qss_file_path: str):
        with open(qss_file_path, "r") as qss_file:
            self.setStyleSheet(qss_file.read())

    """Override"""
    def closeEvent(self, event):
        super().closeEvent(event)
        if (
            self.record_button.has_recording_started 
            and not self.record_button.recorder_stop_event.is_set()
        ):
            self.record_button.recorder_stop_event.set()
            if self.record_button.recording_area_selector.recording_area_border is not None:
                self.record_button.recording_area_selector.recording_area_border.destroy()
        if self.open_editor_button.get_editor_window_widget() is not None:
            self.open_editor_button.get_editor_window_widget().close()

    """Override"""
    def resizeEvent(self, event):
        if self.first_window_resize_event:
            self.setFixedSize(event.size())
            self.first_window_resize_event = False
        super().resizeEvent(event)

    @Slot()
    def __on_hotkey_detected(self, hotkey_name: str):
        if hotkey_name == "screenshot":
            self.screenshot_button.on_hotkey_pressed()
        elif hotkey_name == "start_stop_recording":
            self.record_button.on_hotkey_pressed()
