import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog

from .RenderingProgressDialog_ui import Ui_RenderingProgressDialog


class RenderingProgressDialog(QDialog, Ui_RenderingProgressDialog):
    """Shows progress of rendering when saving from the editor."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setFixedSize(self.size())
        self.close_button.clicked.connect(self.close)
        self.__is_rendering_finished = False
        self.__is_final_file_rendering_text_set = False
        self.__is_temp_cut_video_rendering_text_set = False
        self.__is_cropping_progress_text_set = False
        self.__final_file_rendering_text = "Rendering..."
        self.__temp_cut_video_rendering_text = "Preparing video for cropping..."
        self.__cropping_text = "Cropping..."
        self.__rendering_complete_text = "File successfully rendered and saved!"

    """Override"""
    def keyPressEvent(self, event):
        if not self.__is_rendering_finished:
            if event.key() == Qt.Key_Escape:
                event.ignore()
        else:
            super().keyPressEvent(event)

    @Slot()
    def final_file_rendering_progress_received(self, progress_percentage):
        if not self.__is_final_file_rendering_text_set:
            self.status_message_label.setText(self.__final_file_rendering_text)
            self.__is_final_file_rendering_text_set = True
        self.progress_bar.setValue(progress_percentage)

    @Slot()
    def temp_cut_video_rendering_progress_received(self, progress_percentage):
        if not self.__is_temp_cut_video_rendering_text_set:
            self.status_message_label.setText(self.__temp_cut_video_rendering_text)
            self.__is_temp_cut_video_rendering_text_set = True
        self.progress_bar.setValue(progress_percentage)

    @Slot()
    def cropping_progress_received(self, progress_percentage):
        if not self.__is_cropping_progress_text_set:
            self.status_message_label.setText(self.__cropping_text)
            self.__is_cropping_progress_text_set = True
        self.progress_bar.setValue(progress_percentage)

    @Slot()
    def rendering_finished(self, file_path):
        self.status_message_label.setText(self.__rendering_complete_text)
        self.close_button.setEnabled(True)
        self.__is_rendering_finished = True
        dir_path = os.path.dirname(file_path)
        os.startfile(dir_path)
