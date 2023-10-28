import threading
import queue

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtWidgets import QApplication

from ._notification_widget import Notification


class NotificationManager(QThread):

    ready_to_display_signal = Signal(object)

    def __init__(self):
        super().__init__()
        self.__app = QApplication.instance() or QApplication([])
        self.__notifications = []
        self.__x_padding = 25
        self.__y_padding = 0
        self.__notification_queue = queue.Queue()
        self.__notification_available_flag = threading.Event()

    def run(self):
        while True:
            self.__notification_available_flag.wait()
            if not self.__notification_queue.empty():
                notification = self.__notification_queue.get()
                last_notification = self.__notifications[-1] if self.__notifications else None
                notification.set_position(
                    *self.__calculate_position(
                        notification,
                        last_notification
                    )
                )
                notification.closed_signal.connect(self.__on_notification_closed)
                self.__notifications.append(notification)
                self.ready_to_display_signal.emit(notification)
            else:
                self.__notification_available_flag.clear()

    def put_in_queue(self, message, time_ms, image):
        self.__notification_queue.put(Notification(message, time_ms, image))
        if not self.__notification_available_flag.is_set():
            self.__notification_available_flag.set()

    @Slot()
    def __on_notification_closed(self, notification):
        self.__notifications.remove(notification)
        self.__rearrange_notifications()

    def __calculate_position(self, new_notification, last_notification):
        if last_notification is None:
            return self.__calculate_bottom_most_position(new_notification)

        last_notification_x = last_notification.x()
        last_notification_y = last_notification.y()
        new_notification_h = new_notification.height()
        _, screen_size_diff_h = self.__get_screen_size_difference()
        return (
            last_notification_x,
            last_notification_y - new_notification_h - self.__y_padding - screen_size_diff_h
        )

    def __calculate_bottom_most_position(self, notification):
        available_w, available_h = self.__get_available_screen_size()
        size_diff_w, size_diff_h = self.__get_screen_size_difference()
        return (
            available_w - notification.width() - size_diff_w - self.__x_padding,
            available_h - notification.height() - size_diff_h - self.__y_padding
        )
    
    def __rearrange_notifications(self):
        for i, notification in enumerate(self.__notifications):
            if i == 0:
                notification.set_position(
                    *self.__calculate_bottom_most_position(notification)
                )
            else:
                last_notification = self.__notifications[i-1]
                notification.set_position(
                    *self.__calculate_position(
                        notification,
                        last_notification
                    )
                )

    def __get_available_screen_size(self):
        return self.__app.primaryScreen().availableSize().toTuple()
    
    def __get_total_screen_size(self):
        return self.__app.primaryScreen().size().toTuple()
    
    def __get_screen_size_difference(self):
        total_w, total_h = self.__get_total_screen_size()
        available_w, available_h = self.__get_available_screen_size()
        return total_w - available_w, total_h - available_h
