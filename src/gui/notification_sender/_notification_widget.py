from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication

from ._NotificationWidget_ui import Ui_NotificationWidget


class Notification(QWidget, Ui_NotificationWidget):

    def __init__(self, notification_message):
        super().__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.notification_label.setText(notification_message)
        self.__app = QApplication.instance() or QApplication([])
        self.__x_padding = 25
        self.__y_padding = 0
        self.move(*self.__calculate_position())

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
