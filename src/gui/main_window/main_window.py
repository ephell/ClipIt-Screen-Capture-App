from logger import GlobalLogger
log = GlobalLogger.LOGGER

from time import sleep
import threading

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QMainWindow

from .MainWindow_ui import Ui_MainWindow
from .buttons.settings_button.settings_window.hotkeys.hotkey_listener import HotkeyListener
from .system_tray.system_tray import SystemTray
from gui.main_window.buttons.debug_button.debug_button import DebugButton


class MainWindow(QMainWindow, Ui_MainWindow):

    ready_to_exit_signal = Signal()

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.__set_stylesheet("src/gui/main_window/MainWindow.qss")
        self.app = app
        self.first_window_resize_event = True
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.start()
        self.system_tray = SystemTray(self)
        self.system_tray.show()
        self.__connect_signals_and_slots()
        # Debug button for various prints to console (not in MainWindow.ui)
        # self.debug_button = DebugButton(self)
        # self.verticalLayout_4.addWidget(self.debug_button)
        # self.debug_button.clicked.connect(self.debug_button.on_debug_button_clicked)
    
    def __set_stylesheet(self, qss_file_path: str):
        with open(qss_file_path, "r") as qss_file:
            self.setStyleSheet(qss_file.read())

    def __connect_signals_and_slots(self):
        # Main window
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
        # Hotkey listener
        self.hotkey_listener.hotkey_detected_signal.connect(
            self.__on_hotkey_detected
        )
        # System tray
        self.system_tray.action_start_stop_recording.triggered.connect(
            self.record_button.on_record_button_clicked
        )
        self.system_tray.action_screenshot.triggered.connect(
            self.screenshot_button.on_screenshot_button_clicked
        )
        self.system_tray.action_open_editor.triggered.connect(
            self.open_editor_button.on_open_editor_button_clicked
        )
        self.system_tray.action_open_capture_folder.triggered.connect(
            self.open_capture_folder_button.on_open_capture_folder_button_clicked
        )
        self.system_tray.action_settings.triggered.connect(
            self.settings_button.on_settings_button_clicked
        )
        self.system_tray.request_exit_signal.connect(
            self.__on_request_exit
        )
        self.ready_to_exit_signal.connect(
            self.system_tray.on_ready_to_exit
        )

    """Override"""
    def closeEvent(self, event):
        event.ignore()
        self.hide()

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

    @Slot()
    def __on_request_exit(self):
        if (
            self.record_button.has_recording_started 
            and not self.record_button.recorder_stop_event.is_set()
        ):
            checker = _OnExitThreadChecker(
                self.ready_to_exit_signal
            )
            checker.start()
            self.record_button.on_record_button_clicked()
        if not self.record_button.is_recording_thread_alive():
            self.ready_to_exit_signal.emit()


class _OnExitThreadChecker(threading.Thread):

    def __init__(self, ready_to_exit_signal):
        super().__init__()
        self.ready_to_exit_signal = ready_to_exit_signal
        self.__sleep_time = 0.5

    def run(self):
        while True:
            thread_names = [thread.getName() for thread in threading.enumerate()]
            if "Recorder" not in thread_names:
                 self.ready_to_exit_signal.emit()
                 break
            sleep(self.__sleep_time)
