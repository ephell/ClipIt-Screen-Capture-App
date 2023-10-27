from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QStyle

from ._notification_widget import Notification


class NotificationManager:
    __instance = None
    
    __notifications = []
    __app = None
    __x_padding = 25
    __y_padding = 0

    __INFORMATION_ICON_16x16 = None
    __INFORMATION_ICON_32x32 = None
    __WARNING_ICON_16x16 = None
    __WARNING_ICON_32x32 = None
    __CRITICAL_ICON_16x16 = None
    __CRITICAL_ICON_32x32 = None
    __QUESTION_ICON_16x16 = None
    __QUESTION_ICON_32x32 = None

    def __new__(self):
        if self.__instance is None:
            self.__instance = super().__new__(self)
            self.__instance.__init()
        return self.__instance

    def __init(self):
        self.__app = QApplication.instance() or QApplication([])
        self.__notifications = []
        self.__x_padding = 25
        self.__y_padding = 0
        self.__set_icon_pixmaps()

    def send_notification(self, message, time_ms, type="information"):
        if type == "information":
            self.__send_notification(message, time_ms, self.__INFORMATION_ICON_16x16)
        elif type == "warning":
            self.__send_notification(message, time_ms, self.__WARNING_ICON_16x16)
        elif type == "critical":
            self.__send_notification(message, time_ms, self.__CRITICAL_ICON_16x16)
        elif type == "question":
            self.__send_notification(message, time_ms, self.__QUESTION_ICON_16x16)
        else:
            raise ValueError(f"Invalid notification type: {type}")

    def __send_notification(self, message, time_ms, icon):
        last_notification = self.__notifications[-1] if self.__notifications else None
        new_notification = Notification(message, time_ms, icon)
        new_notification.set_position(
            *self.__calculate_position(
                new_notification,
                last_notification
            )
        )
        new_notification.closed_signal.connect(self.__on_notification_closed)
        self.__notifications.append(new_notification)
        new_notification.show()

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

    def __set_icon_pixmaps(self):
        style = self.__app.style()

        information_icon = style.standardIcon(QStyle.SP_MessageBoxInformation)
        sizes = information_icon.availableSizes()
        self.__INFORMATION_ICON_16x16 = information_icon.pixmap(sizes[0])
        self.__INFORMATION_ICON_32x32 = information_icon.pixmap(sizes[1])

        warning_icon = style.standardIcon(QStyle.SP_MessageBoxWarning)
        sizes = warning_icon.availableSizes()
        self.__WARNING_ICON_16x16 = warning_icon.pixmap(sizes[0])
        self.__WARNING_ICON_32x32 = warning_icon.pixmap(sizes[1])

        critical_icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        sizes = critical_icon.availableSizes()
        self.__CRITICAL_ICON_16x16 = critical_icon.pixmap(sizes[0])
        self.__CRITICAL_ICON_32x32 = critical_icon.pixmap(sizes[1])

        question_icon = style.standardIcon(QStyle.SP_MessageBoxQuestion)
        sizes = question_icon.availableSizes()
        self.__QUESTION_ICON_16x16 = question_icon.pixmap(sizes[0])
        self.__QUESTION_ICON_32x32 = question_icon.pixmap(sizes[1])
