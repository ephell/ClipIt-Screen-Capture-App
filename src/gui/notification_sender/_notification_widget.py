from datetime import datetime

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import QWidget

from ._NotificationWidget_ui import Ui_NotificationWidget


class Notification(QWidget, Ui_NotificationWidget):

    closed_signal = Signal(object)

    def __init__(self, message, time_ms, icon_q_pixmap):
        super().__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.message_label.setMaximumSize(self.maximumSize())
        self.message_label.setMinimumSize(self.minimumSize())
        self.message_label.setText(f"<b><i>[{self.__get_current_time()}]</i></b> <i>{message}</i>")
        self.time_ms = time_ms
        self.setWindowIcon(icon_q_pixmap)
        # This is needed so that self.width() and self.height() return
        # the correct values with wrapped text taken into account.
        # If omitted, these methods will return the original size and 
        # this will cause incorrect positioning of the widget.
        self.setMinimumSize(self.sizeHint())
        # ------------------------------------------------------------
        self.setMaximumHeight(self.height())

    """Override"""
    def closeEvent(self, event):
        self.closed_signal.emit(self)
        super().closeEvent(event)

    """Override"""
    def show(self):
        super().show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        QTimer.singleShot(self.time_ms, self.close)

    def set_position(self, x, y):
        self.move(x, y)

    def __get_current_time(self):
        return datetime.now().strftime('%H:%M:%S.%f')[:-3]
