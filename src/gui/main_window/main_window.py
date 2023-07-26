from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
import os
from time import perf_counter
import threading

from PySide6.QtCore import Qt, Slot, QThread
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QPushButton, QFileDialog
)

from gui.editor.editor import Editor
from .final_file_generation_dialog.final_file_generation_dialog import FinalFileGenerationDialog
from recorder.recorder import Recorder
from settings.settings import Settings
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.first_window_resize_event = True
        self.is_recorder_running = False
        self.recorder_stop_event = None
        self.debug_button = QPushButton("Print Debug Info", self)
        self.debug_button.setObjectName("debug_button")
        self.central_layout.addWidget(self.debug_button)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.select_area_button.clicked.connect(
            self.select_area_button.on_select_area_clicked
        )
        self.start_button.clicked.connect(self.__on_start_button_clicked)
        self.stop_button.clicked.connect(self.__on_stop_button_clicked)
        self.open_editor_button.clicked.connect(
            self.__on_open_editor_button_clicked
        )
        self.open_capture_folder_button.clicked.connect(
            self.__on_open_capture_folder_button_clicked
        )
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
        if self.is_recorder_running and not self.recorder_stop_event.is_set():
            self.recorder_stop_event.set()
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
        print(
            "----------------------------------------\n"
            + "".join(repr(w) + "\n" for w in self.app.allWidgets())
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
    def __on_start_button_clicked(self):
        if (
            not self.is_recorder_running
            and self.select_area_button.recording_area_border is not None
        ):
            self.is_recorder_running = True
            self.video_capture_duration_label.setText("Starting ...")
            self.start_button.setEnabled(False)
            self.select_area_button.setEnabled(False)

            self.recorder_stop_event = threading.Event()
            self.recorder = Recorder(
                record_video=True,
                record_loopback=Settings.get_audio_preferences().getboolean("RECORD_LOOPBACK"),
                record_microphone=Settings.get_audio_preferences().getboolean("RECORD_MICROPHONE"),
                stop_event=self.recorder_stop_event,
                region=[*self.select_area_button.get_area_coords()],
                monitor=self.select_area_button.get_monitor(),
                fps=30
            )
            self.recorder.recording_started_signal.connect(
                self.__on_recording_started
            )
            self.recorder.recorder_stop_event_set_signal.connect(
                self.__on_recorder_stop_event_set
            )
            self.recorder.file_generation_finished_signal.connect(
                self.__on_file_generation_finished
            )
            self.video_capture_duration_label_updater = _VideoCaptureDurationLabelUpdater(
                self.video_capture_duration_label,
                self.recorder_stop_event
            )
            self.recorder.start()
            self.video_capture_duration_label_updater.start()

    @Slot()
    def __on_stop_button_clicked(self):
        if self.select_area_button.recording_area_border is not None:
            if self.recorder_stop_event is not None:
                self.recorder_stop_event.set()
                self.recorder_stop_event = None
            self.is_recorder_running = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.select_area_button.setEnabled(True)
            self.select_area_button.recording_area_border.destroy()
            self.select_area_button.recording_area_border = None

    @Slot()
    def __on_recording_started(self, start_time):
        self.video_capture_duration_label_updater.set_start_time(start_time)
        self.stop_button.setEnabled(True)

    @Slot()
    def __on_recorder_stop_event_set(self, total_encoding_steps):
        self.final_file_generation_dialog = FinalFileGenerationDialog(
            recorder=self.recorder,
            total_steps=total_encoding_steps,
            parent=self
        )
        self.final_file_generation_dialog.show()

    @Slot()
    def __on_file_generation_finished(self, file_path):
        message_box = _FileGenerationCompleteMessageBox(file_path)
        user_choice = message_box.exec()
        if user_choice == QMessageBox.Yes:
            if self.__get_editor() is None:
                self.editor = Editor(file_path)
                self.editor.source_file_changed_signal.connect(
                    self.__on_editor_source_file_changed
                )
                self.editor.show()
            else:
                _EditorAlreadyOpenMessageBox(self).exec()
        message_box.deleteLater()

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
        if self.__get_editor() is not None:
            self.__get_editor().close()
        self.editor = Editor(path)
        self.editor.source_file_changed_signal.connect(
            self.__on_editor_source_file_changed
        )
        self.editor.show()            

    @Slot()
    def __on_open_capture_folder_button_clicked(self):
        os.startfile(Settings.get_capture_dir_path())


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
                elapsed_time = current_time - self.start_time
                seconds = int(elapsed_time)
                minutes = seconds // 60
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


class _FileGenerationCompleteMessageBox(QMessageBox):

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setWindowTitle("File Generation Complete")
        self.setText(
            "File saved to: \n"
            f"{file_path}"
        )
        self.setInformativeText("Open the file in the editor?")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        self.setIcon(QMessageBox.Information)
