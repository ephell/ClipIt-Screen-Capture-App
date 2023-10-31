from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QPushButton, QFileDialog, QMessageBox

from src.settings.settings import Settings


class UploadButton(QPushButton):

    upload_file_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def on_click(self):
        file_dialog = _UploadFileDialog(self)
        while True:
            if file_dialog.exec() == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                if file_path.lower().endswith(".mp4"):
                    self.upload_file_signal.emit(file_path)
                    break
                else:
                    QMessageBox.critical(
                        self, 
                        "Invalid File Type", 
                        "Please select a file with '.mp4' extension."
                    )
            else:
                break


class _UploadFileDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select a file to upload ...")
        self.setNameFilter("Video Files (*.mp4)")
        self.setFileMode(QFileDialog.ExistingFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory(Settings.get_capture_dir_path())
