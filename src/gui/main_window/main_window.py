from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
import os
import threading

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QMessageBox, QPushButton, QFileDialog
)

from .buttons.select_area_button.main_logic import SelectAreaButtonLogic
from gui.editor.editor import Editor
from .final_file_generation_dialog.final_file_generation_dialog import FinalFileGenerationDialog
from recorder.recorder import Recorder
from settings import Paths
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.app = app
        self.first_resize_event = True
        self._select_area_button_logic = SelectAreaButtonLogic()
        self.is_recording = False
        self.stop_event = None
        self.debug_button = QPushButton("Print Debug Info", self)
        self.debug_button.setObjectName("debug_button")
        self.central_layout.addWidget(self.debug_button)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.select_area_button.clicked.connect(
            self._select_area_button_logic.on_select_area_clicked
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
            if self._select_area_button_logic.area_selector is not None:
                self._select_area_button_logic.area_selector.close()

    """Override"""
    def closeEvent(self, event):
        super().closeEvent(event)
        if self.is_recording and not self.stop_event.is_set():
            self.stop_event.set()
        if self.__get_editor() is not None:
            self.__get_editor().close()

    def __get_editor(self):
        for widget in self.app.allWidgets():
            if isinstance(widget, Editor):
                return widget
        return None

    """Override"""
    def resizeEvent(self, event):
        if self.first_resize_event:
            self.setFixedSize(event.size())
            self.first_resize_event = False
        super().resizeEvent(event)

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
    def __on_stop_button_clicked(self):
        if self._select_area_button_logic.recording_area_border is not None:
            self._select_area_button_logic.recording_area_border.destroy()
            self._select_area_button_logic.recording_area_border = None
            self.stop_event.set()
            self.stop_event = None
            self.is_recording = False

    @Slot()
    def __on_start_button_clicked(self):
        if not self.is_recording:
            if self._select_area_button_logic.recording_area_border is not None:
                self.is_recording = True
                self.stop_event = mp.Event()
                self.recorder = Recorder(
                    record_video=True,
                    record_loopback=True,
                    record_microphone=True,
                    stop_event=self.stop_event,
                    region=[*self._select_area_button_logic.get_area_coords()],
                    monitor=self._select_area_button_logic.get_monitor(),
                    fps=30
                )
                self.recorder.recorder_stop_event_set_signal.connect(
                    self.__on_recorder_stop_event_set
                )
                self.recorder.file_generation_finished_signal.connect(
                    self.__on_file_generation_finished
                )
                self.recorder.start()
        else:
            log.error("Recording process is already running.")

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
                self.editor.show()
            else:
                _EditorAlreadyOpenMessageBox(self).exec()
        message_box.deleteLater()

    @Slot()
    def __on_open_editor_button_clicked(self):
        if self.__get_editor() is None:
            file_dialog = _OpenFileInEditorDialog(self)
            user_choice = file_dialog.exec()
            if user_choice == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                self.editor = Editor(file_path)
                self.editor.show()
            file_dialog.deleteLater()
        else:
            _EditorAlreadyOpenMessageBox(self).exec()

    @Slot()
    def __on_open_capture_folder_button_clicked(self):
        os.startfile(Paths.RECORDINGS_DIR)


class _OpenFileInEditorDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to open ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Paths.RECORDINGS_DIR)


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
