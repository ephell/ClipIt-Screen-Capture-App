from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QPushButton, QFileDialog

from settings.settings import Settings


class UploadButton(QPushButton):

    upload_file_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def on_click(self):
        file_dialog = _UploadFileDialog(self)
        user_choice = file_dialog.exec()
        if user_choice == QFileDialog.Accepted:
            file_path = file_dialog.selectedFiles()[0]
            self.upload_file_signal.emit(file_path)


class _UploadFileDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to upload ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Settings.get_capture_dir_path())
