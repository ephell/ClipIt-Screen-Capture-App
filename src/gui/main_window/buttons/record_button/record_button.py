from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QPushButton, QMessageBox

import threading

from gui.main_window.final_file_generation_dialog.final_file_generation_dialog import FinalFileGenerationDialog
from settings.settings import Settings
from recorder.recorder import Recorder
from ._recording_area_selector import RecordingAreaSelector


class RecordButton(QPushButton):

    open_editor_after_file_generation_finished_signal = Signal(str)
    recording_starting_signal = Signal()
    recording_started_signal = Signal(float, threading.Event)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_recorder_running = False
        self.recorder_stop_event = None

    def __start_recording(self):
        self.recording_starting_signal.emit()
        self.setEnabled(False)
        self.is_recorder_running = True

        self.recorder_stop_event = threading.Event()
        self.recorder = Recorder(
            record_video=True,
            record_loopback=Settings.get_audio_preferences().getboolean("RECORD_LOOPBACK"),
            record_microphone=Settings.get_audio_preferences().getboolean("RECORD_MICROPHONE"),
            stop_event=self.recorder_stop_event,
            region=[*self.recording_area_selector.get_area_coords()],
            monitor=self.recording_area_selector.get_monitor(),
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
        self.recorder.start()

    def __stop_recording(self):
        if self.recording_area_selector.recording_area_border is not None:
            if self.recorder_stop_event is not None:
                self.recorder_stop_event.set()
                self.recorder_stop_event = None
            self.is_recorder_running = False
            self.recording_area_selector.recording_area_border.destroy()
            self.recording_area_selector.recording_area_border = None

    @Slot()
    def on_record_button_clicked(self):
        if not self.is_recorder_running:
            self.recording_area_selector = RecordingAreaSelector()
            self.recording_area_selector.area_selection_finished_signal.connect(
                self.__on_area_selection_finished
            )
            self.recording_area_selector.start_selection()
        if self.is_recorder_running:
            self.__stop_recording()

    @Slot()
    def __on_area_selection_finished(self):
        self.__start_recording()

    @Slot()
    def __on_recording_started(self, start_time):
        self.recording_started_signal.emit(start_time, self.recorder_stop_event)
        self.setEnabled(True)
        if self.recording_area_selector.recording_area_border is not None:
            self.recording_area_selector.recording_area_border.update_color((255, 0, 0))

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
            self.open_editor_after_file_generation_finished_signal.emit(file_path)
        message_box.deleteLater()


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
