from logger import GlobalLogger
log = GlobalLogger.LOGGER

from time import perf_counter

from PySide6.QtCore import Qt, Slot, QThread
from PySide6.QtWidgets import QMainWindow

from .Ui_MainWindow import Ui_MainWindow
from gui.main_window.buttons.debug_button.debug_button import DebugButton


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.first_window_resize_event = True
        self.__connect_signals_and_slots()
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
        self.record_button.recording_starting_signal.connect(
            self.__on_recording_starting
        )
        self.record_button.recording_started_signal.connect(
            self.__on_recording_started
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
 
    @Slot()
    def __on_recording_starting(self):
        self.video_capture_duration_label.setText("Starting...")

    @Slot()
    def __on_recording_started(self, start_time, recorder_stop_event):
        self.video_capture_duration_label_updater = _VideoCaptureDurationLabelUpdater(
            self.video_capture_duration_label,
            recorder_stop_event
        )
        self.video_capture_duration_label_updater.set_start_time(start_time)
        self.video_capture_duration_label_updater.start()


class _VideoCaptureDurationLabelUpdater(QThread):

    def __init__(self, time_label, stop_event):
        super().__init__()
        self.time_label = time_label
        self.recorder_stop_event = stop_event
        self.start_time = None

    def run(self):
        while not self.recorder_stop_event.is_set():
            if self.start_time is not None:
                current_time = perf_counter()
                elapsed_time = int(current_time - self.start_time)
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                self.time_label.setText(f"{minutes:02d}:{seconds:02d}")

    def set_start_time(self, start_time):
        self.start_time = start_time
