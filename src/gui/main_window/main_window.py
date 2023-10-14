from logger import GlobalLogger
log = GlobalLogger.LOGGER

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from .Ui_MainWindow import Ui_MainWindow
from gui.main_window.buttons.debug_button.debug_button import DebugButton

from .hotkey_listener.hotkey_listener import HotkeyListener


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.first_window_resize_event = True
        self.__connect_signals_and_slots()
        self.hotkey_listener = HotkeyListener()
        self.hotkey_listener.start()
        # Debug button for various prints to console (not in MainWindow.ui)
        self.debug_button = DebugButton(self)
        self.central_layout.addWidget(self.debug_button)
        self.debug_button.clicked.connect(self.debug_button.on_debug_button_clicked)

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

    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.select_area_button.area_selector is not None:
                try:
                    self.select_area_button.area_selector.close()
                except RuntimeError:
                    log.info("Area selector already closed.")

    """Override"""
    def closeEvent(self, event):
        super().closeEvent(event)
        if (
            self.record_button.is_recorder_running 
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
