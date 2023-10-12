from logger import GlobalLogger
log = GlobalLogger.LOGGER

import os
from time import perf_counter
import threading

from PySide6.QtCore import Qt, Slot, QThread
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QPushButton, QFileDialog
)

from gui.editor.editor import Editor
from gui.settings.settings import Settings as SettingsWindow
from settings.settings import Settings
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.first_window_resize_event = True
        self.debug_button = QPushButton("Print Debug Info", self)
        self.debug_button.setObjectName("debug_button")
        self.central_layout.addWidget(self.debug_button)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.record_button.clicked.connect(
            self.record_button.on_record_button_clicked
        )
        self.record_button.open_editor_after_file_generation_finished_signal.connect(
            self.__on_file_generation_finished
        )
        self.record_button.recording_starting_signal.connect(
            self.__on_recording_starting
        )
        self.record_button.recording_started_signal.connect(
            self.__on_recording_started
        )
        self.open_editor_button.clicked.connect(
            self.__on_open_editor_button_clicked
        )
        self.open_capture_folder_button.clicked.connect(
            self.__on_open_capture_folder_button_clicked
        )
        self.screenshot_button.clicked.connect(
            self.screenshot_button.on_screenshot_button_clicked
        )
        self.settings_button.clicked.connect(self.__on_settings_button_clicked)
        self.debug_button.clicked.connect(self.__on_debug_button_clicked)

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
        if self.__get_editor() is not None:
            self.__get_editor().close()

    """Override"""
    def resizeEvent(self, event):
        if self.first_window_resize_event:
            self.setFixedSize(event.size())
            self.first_window_resize_event = False
        super().resizeEvent(event)

    def __get_editor(self):
        for widget in self.app.allWidgets():
            if isinstance(widget, Editor):
                return widget
        return None

    @Slot()
    def __on_debug_button_clicked(self):
        print(threading.enumerate())
        
        # Check if specific widget exists
        widgets = [
            w for w in self.app.allWidgets() if w.objectName() == "Settings"
        ]
        print(
            "----------------------------------------\n"
            + "".join(repr(w) + "\n" for w in widgets)
            + "----------------------------------------"
        )

        # def get_signals(source):
        #     cls = source if isinstance(source, type) else type(source)
        #     signal = type(Signal())
        #     for subcls in cls.mro():
        #         clsname = f'{subcls.__module__}.{subcls.__name__}'
        #         for key, value in sorted(vars(subcls).items()):
        #             if isinstance(value, signal):
        #                 print(f'{key} [{clsname}]')
 
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

    @Slot()
    def __on_open_editor_button_clicked(self):
        if self.__get_editor() is None:
            file_dialog = _OpenFileInEditorDialog(self)
            while True:
                if file_dialog.exec() == QFileDialog.Accepted:
                    file_path = file_dialog.selectedFiles()[0]
                    if file_path.lower().endswith(".mp4"):
                        self.editor = Editor(file_path)
                        self.editor.source_file_changed_signal.connect(
                            self.__on_editor_source_file_changed
                        )
                        self.editor.show()
                        break
                    else:
                        QMessageBox.critical(
                            self, 
                            "Invalid File Type", 
                            "Please select a file with '.mp4' extension."
                        )
                else:
                    break
            file_dialog.deleteLater()
        else:
            _EditorAlreadyOpenMessageBox(self).exec()

    @Slot()
    def __on_editor_source_file_changed(self, path):
        self.editor = Editor(path)
        self.editor.source_file_changed_signal.connect(
            self.__on_editor_source_file_changed
        )
        self.editor.show()            

    @Slot()
    def __on_open_capture_folder_button_clicked(self):
        os.startfile(Settings.get_capture_dir_path())

    @Slot()
    def __on_settings_button_clicked(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    @Slot()
    def __on_file_generation_finished(self, file_path):
        if self.__get_editor() is None:
            self.editor = Editor(file_path)
            self.editor.source_file_changed_signal.connect(
                self.__on_editor_source_file_changed
            )
            self.editor.show()
        else:
            _EditorAlreadyOpenMessageBox(self).exec()


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


class _OpenFileInEditorDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to open ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Settings.get_capture_dir_path())


class _EditorAlreadyOpenMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Editor Already Open")
        self.setText("Editor is already open.")
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)
