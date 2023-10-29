from datetime import datetime
import os

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap

from ._NotificationWidget_ui import Ui_NotificationWidget
from settings.settings import Settings


class Notification(QWidget, Ui_NotificationWidget):

    closed_signal = Signal(object)

    def __init__(self, message, time_ms, q_image, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.Tool | Qt.MSWindowsFixedSizeDialogHint)
        self.message_label.setMaximumSize(self.maximumSize())
        self.message_label.setMinimumSize(self.minimumSize())
        self.message_label.setText(f"<b><i>[{self.__get_current_time()}]</i></b> <i>{message}</i>")
        self.time_ms = time_ms

        self.q_image = q_image
        if self.q_image is not None:
            self.image_label = QLabel(self)
            self.image_label.setMinimumSize(self.minimumSize())
            self.q_image = self.q_image.scaled(
                self.image_label.width(),
                self.image_label.width(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(QPixmap.fromImage(self.q_image))
            self.verticalLayout.addWidget(self.image_label)
    
        # This is needed so that self.width() and self.height() return
        # the correct values with wrapped text taken into account.
        # If omitted, these methods will return the original size and 
        # this will cause incorrect positioning of the widget.
        self.setMinimumSize(self.sizeHint())

    """Override"""
    def closeEvent(self, event):
        self.closed_signal.emit(self)
        super().closeEvent(event)

    """Override"""
    def show(self):
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        super().show()
        QTimer.singleShot(self.time_ms, self.close)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.q_image is not None:
                os.startfile(Settings.get_capture_dir_path())

    def set_position(self, x, y):
        self.move(x, y)

    def __get_current_time(self):
        return datetime.now().strftime('%H:%M:%S.%f')[:-3]
