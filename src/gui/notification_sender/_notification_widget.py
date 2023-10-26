from PySide6.QtCore import Qt, QTimer, Slot, Signal
from PySide6.QtWidgets import QWidget, QApplication

from ._NotificationWidget_ui import Ui_NotificationWidget


class Notification(QWidget, Ui_NotificationWidget):

    closed_signal = Signal()

    def __init__(self, message, time_ms, icon_q_pixmap):
        super().__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.message_label.setMaximumSize(self.maximumSize())
        self.message_label.setMinimumSize(self.minimumSize())
        self.message_label.setText(message)
        self.setWindowIcon(icon_q_pixmap)
        self.__app = QApplication.instance() or QApplication([])
        self.__x_padding = 25
        self.__y_padding = 0
        # This is needed so that self.width() and self.height() return
        # the correct values with wrapped text taken into account.
        # If omitted, these methods will return the original size and 
        # this will cause incorrect positioning of the widget.
        self.setMinimumSize(self.sizeHint())
        # ------------------------------------------------------------
        self.setMaximumHeight(self.height())
        self.move(*self.__calculate_position())
        self.show()
        QTimer.singleShot(time_ms, self.close)

    """Override"""
    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)

    def __calculate_position(self):
        available_w, available_h = self.__get_available_screen_size()
        size_diff_w, size_diff_h = self.__get_screen_size_difference()
        return (
            available_w - self.width() - size_diff_w - self.__x_padding,
            available_h - self.height() - size_diff_h - self.__y_padding
        )

    def __get_available_screen_size(self):
        return self.__app.primaryScreen().availableSize().toTuple()

    def __get_total_screen_size(self):
        return self.__app.primaryScreen().size().toTuple()

    def __get_screen_size_difference(self):
        total_w, total_h = self.__get_total_screen_size()
        available_w, available_h = self.__get_available_screen_size()
        return total_w - available_w, total_h - available_h
