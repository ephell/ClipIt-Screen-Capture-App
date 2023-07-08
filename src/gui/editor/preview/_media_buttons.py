from PySide6.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QDialog, QFileDialog, QMessageBox
)

from editor import Editor


class MediaButtons(QWidget):

    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.media_player = media_player
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button = QPushButton("Reset", self)
        self.stop_button.clicked.connect(self.media_player.stop)
        self.render_and_save_button = _RenderAndSave(self.media_player, self)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.render_and_save_button)
        self.setLayout(self.layout)


class _RenderAndSave(QPushButton):

    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.setText("Render and Save")
        self.media_player = media_player
        self.clicked.connect(self.on_click)

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
                    Editor.cut_and_save_video(
                        self.__get_start_time(),
                        self.__get_end_time(),
                        source_file_path,
                        new_file_path
                    )
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


class _RenderAndSaveDialog(QFileDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QFileDialog.AnyFile)
        self.setViewMode(QFileDialog.Detail)
        self.setDirectory("C:/Users/drema/Desktop/Programming/ClipIt/recordings")
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
