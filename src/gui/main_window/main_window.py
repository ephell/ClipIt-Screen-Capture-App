from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QMainWindow, QMessageBox, QPushButton, QFileDialog

from .buttons.select_area_button.main_logic import SelectAreaButtonLogic
from gui.editor.editor import Editor
from recorder.recorder import Recorder
from .Ui_MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    finished_recording_signal = Signal(str)

    def __init__(self, app):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("ClipIt")
        self.app = app

        self._select_area_button_logic = SelectAreaButtonLogic()
        self.select_area_button.clicked.connect(
            self._select_area_button_logic.on_select_area_clicked
        )

        self.is_recording = False
        self.start_recording_button.clicked.connect(self.__on_start_clicked)
        
        self.stop_event = None
        self.stop_recording_button.clicked.connect(self.__on_stop_clicked)

        self.finished_recording_signal.connect(self.__on_recording_finished)

        self.open_editor_button.clicked.connect(self.__on_open_editor_clicked)

        self.widget_button = QPushButton("Print All Added Widgets", self)
        self.verticalLayout.addWidget(self.widget_button)
        self.widget_button.clicked.connect(
            lambda: print(
                "----------------------------------------\n"
                + "".join(repr(w) + "\n" for w in self.app.allWidgets())
                + str(self.__get_editor())
                + "----------------------------------------"
            )
        )

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

    def __on_stop_clicked(self):
        if self._select_area_button_logic.recording_area_border is not None:
            self._select_area_button_logic.recording_area_border.destroy()
            self._select_area_button_logic.recording_area_border = None
            self.stop_event.set()
            self.stop_event = None
            self.is_recording = False

    def __on_start_clicked(self):
        if not self.is_recording:
            if self._select_area_button_logic.recording_area_border is not None:
                self.is_recording = True
                self.stop_event = mp.Event()
                recorder = Recorder(
                    record_video=True,
                    record_loopback=True,
                    record_microphone=True,
                    stop_event=self.stop_event,
                    region=[*self._select_area_button_logic.get_area_coords()],
                    monitor=self._select_area_button_logic.get_monitor(),
                    fps=30,
                    recording_finished_callback=self.__recording_finished
                )
                recorder.start()
        else:
            log.error("Recording process is already running.")

    def __recording_finished(self, file_path):
        """Callback for 'Recorder'."""
        self.finished_recording_signal.emit(file_path)

    def __on_recording_finished(self, file_path):
        message_box = _RecordingFinishedMessageBox(file_path)
        user_choice = message_box.exec()
        if user_choice == QMessageBox.Yes:
            self.editor = Editor(file_path)
            self.editor.show()

    def __on_open_editor_clicked(self):
        if self.__get_editor() is None:
            file_dialog = _OpenFileInEditorDialog(self)
            user_choice = file_dialog.exec()
            if user_choice == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                self.editor = Editor(file_path)
                self.editor.show()
            file_dialog.deleteLater()
        else:
            print("Editor is already open.")

    def __get_editor(self):
        for widget in self.app.allWidgets():
            if isinstance(widget, Editor):
                return widget
        return None


class _OpenFileInEditorDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to open ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(
            "C:/Users/drema/Desktop/Programming/ClipIt/recordings"
        )


class _RecordingFinishedMessageBox(QMessageBox):

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.setWindowTitle("Recording Finished")
        self.setText(f"File saved to: {file_path}")
        self.setInformativeText("Do you want to edit the recording?")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
        self.setIcon(QMessageBox.Information)
