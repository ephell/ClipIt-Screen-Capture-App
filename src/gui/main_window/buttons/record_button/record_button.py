from time import perf_counter

from PySide6.QtCore import Slot, Signal, QThread, Qt
from PySide6.QtWidgets import QPushButton, QMessageBox, QMainWindow, QLabel

import threading

from .final_file_generation_dialog.final_file_generation_dialog import FinalFileGenerationDialog
from gui.notification_sender.notification_sender import NotificationSender
from settings.settings import Settings
from recorder.recorder import Recorder
from ._recording_area_selector import RecordingAreaSelector


class RecordButton(QPushButton):

    open_editor_after_file_generation_finished_signal = Signal(str)
    recording_started_signal = Signal()
    recording_stopped_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recorder = None
        self.recorder_stop_event = None
        self.file_generation_choice_event = None
        self.recording_area_selector = None
        self.has_recording_started = False
        self.recording_area_selector = RecordingAreaSelector()
        self.recording_area_selector.area_selection_finished_signal.connect(
            self.__on_area_selection_finished
        )
        self.__notification_sender = NotificationSender()

    def is_recording_thread_alive(self):
        if self.recorder is not None:
            return self.recorder.is_alive()
        return False

    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.recording_area_selector is not None:
                try:
                    self.recording_area_selector.area_selector.close()
                except RuntimeError:
                    # Catches 'Internal C++ object (AreaSelector) already deleted'.
                    # Not a good solution, but passing is not a problem here.
                    pass 
                 
    def __start_recording(self):
        self.__get_capture_duration_label_widget().setText("Starting...")
        self.__notification_sender.send("Starting recording process...", 2000)
        self.__set_stop_recording_icon()
        self.setEnabled(False)
        self.recorder_stop_event = threading.Event()
        self.file_generation_choice_event = threading.Event()
        self.recorder = Recorder(
            record_video=True,
            record_loopback=Settings.get_audio_preferences().getboolean("RECORD_LOOPBACK"),
            record_microphone=Settings.get_audio_preferences().getboolean("RECORD_MICROPHONE"),
            stop_event=self.recorder_stop_event,
            file_generation_choice_event=self.file_generation_choice_event,
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
        self.recorder.file_generation_started_signal.connect(
            self.__on_file_generation_started
        )
        self.recorder.start()

    def __stop_recording(self):
        if self.recording_area_selector.recording_area_border is not None:
            if self.recorder_stop_event is not None:
                self.recorder_stop_event.set()
                self.recorder_stop_event = None
            self.has_recording_started = False
            self.recording_area_selector.recording_area_border.destroy()
            self.recording_area_selector.recording_area_border = None
            self.__set_start_recording_icon()

    def __get_main_window_widget(self):
        widget = self.parent()
        while widget is not None and not isinstance(widget, QMainWindow):
            widget = widget.parent()
        if widget is not None:
            return widget
        return None

    def __get_capture_duration_label_widget(self):
        for w in self.__get_main_window_widget().app.allWidgets():
            if isinstance(w, QLabel) and w.objectName() == "capture_duration_label":
                return w
        return None

    def __set_start_recording_icon(self):
        self.setStyleSheet("""
            #record_button {
                image: url(:/icons/buttons/icons/record_button/1x/baseline_videocam_white_24dp.png);
            }
        """)

    def __set_stop_recording_icon(self):
        self.setStyleSheet("""
            #record_button {
                image: url(:/icons/buttons/icons/record_button/1x/baseline_videocam_off_white_24dp.png);
            }
        """)

    @Slot()
    def on_record_button_clicked(self):
        if not self.has_recording_started:
            if self.recording_area_selector.recording_area_border is None:
                self.recording_area_selector.start_selection()
        if self.has_recording_started:
            self.__stop_recording()

    @Slot()
    def on_hotkey_pressed(self):
        if not self.has_recording_started:
            self.on_record_button_clicked()
        elif self.has_recording_started:
            self.__stop_recording()

    @Slot()
    def __on_area_selection_finished(self):
        self.__start_recording()

    @Slot()
    def __on_recording_started(self, start_time):
        self.recording_started_signal.emit()
        self.__notification_sender.send("Recording started!", 2000)
        self.setEnabled(True)
        self.duration_label_updater = _CaptureDurationLabelUpdater(
            self.__get_capture_duration_label_widget(),
            self.recorder_stop_event
        )
        self.duration_label_updater.set_start_time(start_time)
        self.duration_label_updater.start()
        if self.recording_area_selector.recording_area_border is not None:
            self.recording_area_selector.recording_area_border.update_color((255, 0, 0))
        self.has_recording_started = True

    @Slot()
    def __on_recorder_stop_event_set(self):
        self.recording_stopped_signal.emit()
        message_box = _FileGenerationChoiceMessageBox(self)
        user_choice = message_box.exec()
        if user_choice == QMessageBox.Yes:
            self.recorder.generate_final_file = True
            self.file_generation_choice_event.set()
        else:
            self.recorder.generate_final_file = False
            self.file_generation_choice_event.set()

    @Slot()
    def __on_file_generation_started(self, total_encoding_steps):
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


class _FileGenerationChoiceMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("File Generation Choice")
        self.setText("Recording finished! Render and save the file?")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setDefaultButton(QMessageBox.Yes)
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


class _CaptureDurationLabelUpdater(QThread):

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
