from PySide6.QtCore import Signal, Slot, QThread
from PySide6.QtWidgets import (
    QPushButton, QDialog, QFileDialog, QMessageBox
)

from utilities.video import VideoUtils
from ._progress_loggers import ProgressLoggers
from ._rendering_progress_dialog.rendering_progress_dialog import RenderingProgressDialog
from settings.settings import Settings


class RenderAndSaveButton(QPushButton):

    final_file_rendering_progress_signal = Signal(int)
    temp_cut_video_rendering_progress_signal = Signal(int)
    cropping_progress_signal = Signal(int)
    file_rendered_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.media_player = None
        self.__progress_loggers = ProgressLoggers(
            self.final_file_rendering_progress_signal,
            self.temp_cut_video_rendering_progress_signal,
            self.cropping_progress_signal
        )

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
    
    def __get_crop_area(self):
        area = self.media_player.video_output.get_clip_rect()
        top_l_x = area[0]
        top_l_y = area[1]
        bot_r_x = area[0] + area[2]
        bot_r_y = area[1] + area[3]
        return (top_l_x, top_l_y, bot_r_x, bot_r_y)

    def __render_and_save(self, input_file_path, output_file_path):
        self.rendering_thread = _RenderingThread(
            self.__get_start_time(),
            self.__get_end_time(),
            input_file_path,
            output_file_path,
            self.__get_volume(),
            self.__get_crop_area(),
            self.__progress_loggers
        )
        self.rendering_progress_dialog = RenderingProgressDialog(self)
        self.final_file_rendering_progress_signal.connect(
            self.rendering_progress_dialog.final_file_rendering_progress_received
        )
        self.temp_cut_video_rendering_progress_signal.connect(
            self.rendering_progress_dialog.temp_cut_video_rendering_progress_received
        )
        self.cropping_progress_signal.connect(
            self.rendering_progress_dialog.cropping_progress_received  
        )
        self.rendering_thread.finished.connect(
            lambda: self.rendering_progress_dialog.rendering_finished(
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
            crop_area,
            logger
        ):
        super().__init__()
        self.cut_begin = cut_begin
        self.cut_end = cut_end
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.volume = volume
        self.crop_area = crop_area
        self.logger = logger

    def run(self):
        VideoUtils.render_and_save_video(
            self.input_file_path,
            self.output_file_path,
            self.cut_begin,
            self.cut_end,
            self.volume,
            self.crop_area,
            self.logger
        )
