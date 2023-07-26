from PySide6.QtCore import Signal, Slot, QThread
from PySide6.QtWidgets import (
    QPushButton, QDialog, QFileDialog, QMessageBox
)
from proglog import ProgressBarLogger

from utilities.video import VideoUtils
from ._rendering_progress_dialog.rendering_progress_dialog import RenderingProgressDialog
from settings.settings import Settings


class RenderAndSaveButton(QPushButton):

    rendering_progress_signal = Signal(int)
    file_rendered_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.media_player = None

    def set_media_player(self, media_player):
        self.media_player = media_player

    @Slot()
    def on_click(self):
        file_dialog = _RenderAndSaveDialog(self)
        while True:
            if file_dialog.exec() == QDialog.Accepted:
                new_file_path = file_dialog.selectedFiles()[0]
                source_file_path = self.__get_source_file_path()
                if new_file_path == source_file_path:
                    msg_box = _CannotOverwriteSourceFileMessageBox(self)
                    msg_box.exec()
                else:
                    self.__render_and_save(source_file_path, new_file_path)
                    self.file_rendered_signal.emit()
                    break
            else:
                break
        file_dialog.deleteLater()

    def __get_start_time(self):
        return self.media_player.start_time / 1000.0
    
    def __get_end_time(self):
        return self.media_player.end_time / 1000.0
    
    def __get_source_file_path(self):
        return self.media_player.file_path
    
    def __get_volume(self):
        return self.media_player.audio_output.volume()

    def __render_and_save(self, input_file_path, output_file_path):
        self.logger = _RenderingProgressLogger(self.rendering_progress_signal)
        self.rendering_thread = _RenderingThread(
            self.__get_start_time(),
            self.__get_end_time(),
            input_file_path,
            output_file_path,
            self.__get_volume(),
            self.logger
        )
        self.rendering_progress_dialog = RenderingProgressDialog(self)
        self.rendering_progress_signal.connect(
            self.rendering_progress_dialog.progress_bar.setValue
        )
        self.rendering_thread.finished.connect(
            lambda: self.rendering_progress_dialog.on_rendering_complete(
                output_file_path
            )
        )
        self.rendering_progress_dialog.show()
        self.rendering_thread.start()


class _RenderAndSaveDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QFileDialog.AnyFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Settings.get_capture_dir_path())
        self.setDefaultSuffix("mp4")
        self.setAcceptMode(QFileDialog.AcceptSave)


class _CannotOverwriteSourceFileMessageBox(QMessageBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error")
        self.setText(
            "Cannot overwrite this file. "
            "It is currently in use by another process."
        )
        self.setInformativeText("Please select another file name.")
        self.setStandardButtons(QMessageBox.Ok)
        self.setDefaultButton(QMessageBox.Ok)
        self.setIcon(QMessageBox.Critical)


class _RenderingThread(QThread):

    def __init__(
            self,
            cut_begin,
            cut_end,
            input_file_path,
            output_file_path,
            volume,
            logger
        ):
        super().__init__()
        self.cut_begin = cut_begin
        self.cut_end = cut_end
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.volume = volume
        self.logger = logger

    def run(self):
        VideoUtils.cut_and_save_video(
            self.cut_begin,
            self.cut_end,
            self.input_file_path,
            self.output_file_path,
            self.volume,
            self.logger
        )


class _RenderingProgressLogger(ProgressBarLogger):

    def __init__(self, progress_signal):
        super().__init__()
        self.progress_signal = progress_signal

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "index":
            percentage = (value / self.bars[bar]["total"]) * 100
            self.progress_signal.emit(percentage)
