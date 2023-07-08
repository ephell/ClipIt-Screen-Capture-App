from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog

from .Ui_FinalFileGenerationDialog import Ui_FinalFileGenerationDialog


class FinalFileGenerationDialog(QDialog, Ui_FinalFileGenerationDialog):
    """Dialog that shows the progress of the final file generation process."""

    def __init__(self, recorder, total_steps, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlag(Qt.Window)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(self.size())
        self.recorder = recorder
        self.total_steps = total_steps
        self.current_step = 0
        self.is_first_video_reencoding_signal = True
        self.is_first_audio_merging_signal = True
        self.is_first_video_and_audio_merging_signal = True
        self.is_file_generation_complete = False
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.recorder.video_reencoding_progress_signal.connect(
            self.__on_video_reencoding_progress_signal_received
        )
        self.recorder.audio_merging_progress_signal.connect(
            self.__on_audio_merging_progress_signal_received
        )
        self.recorder.video_and_audio_merging_progress_signal.connect(
            self.__on_video_and_audio_merging_progress_signal_received
        )
        self.recorder.file_generation_finished_signal.connect(
            self.__on_file_generation_finished_signal_received
        )

    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            event.ignore()
        else:
            super().keyPressEvent(event)

    @Slot()
    def __on_video_reencoding_progress_signal_received(self, value):
        self.progress_bar.setValue(value)
        if self.is_first_video_reencoding_signal:
            self.is_first_video_reencoding_signal = False
            self.current_step += 1
            self.status_message_label.setText(
                f"({self.current_step}/{self.total_steps}) "
                "Encoding video frames ..."
            )

    @Slot()
    def __on_audio_merging_progress_signal_received(self, value):
        self.progress_bar.setValue(value)
        if self.is_first_audio_merging_signal:
            self.is_first_audio_merging_signal = False
            self.current_step += 1
            self.status_message_label.setText(
                f"({self.current_step}/{self.total_steps}) "
                "Merging speaker and microphone audio ..."
            )

    @Slot()
    def __on_video_and_audio_merging_progress_signal_received(self, value):
        self.progress_bar.setValue(value)
        if self.is_first_video_and_audio_merging_signal:
            self.is_first_video_and_audio_merging_signal = False
            self.current_step += 1
            self.status_message_label.setText(
                f"({self.current_step}/{self.total_steps}) "
                "Merging video and audio ..."
            )

    @Slot()
    def __on_file_generation_finished_signal_received(self):
        self.close()
