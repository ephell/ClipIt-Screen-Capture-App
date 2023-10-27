from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QStyle

from ._notification_widget import Notification


class NotificationSender:

    __icons = {
        'INFORMATION_ICON_16x16': None,
        'INFORMATION_ICON_32x32': None,
        'WARNING_ICON_16x16': None,
        'WARNING_ICON_32x32': None,
        'CRITICAL_ICON_16x16': None,
        'CRITICAL_ICON_32x32': None,
        'QUESTION_ICON_16x16': None,
        'QUESTION_ICON_32x32': None,
    }

    def __init__(self):
        if any(icon is None for icon in self.__icons.values()):
            self.__get_icon_pixmaps()
        self.__notifications = []
        self.__app = QApplication.instance() or QApplication([])
        self.__x_padding = 25
        self.__y_padding = 0

    def send_information(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["INFORMATION_ICON_16x16"])

    def send_warning(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["WARNING_ICON_16x16"])

    def send_critical(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["CRITICAL_ICON_16x16"])

    def send_question(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["QUESTION_ICON_16x16"])

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

    @Slot()
    def __on_notification_closed(self, notification):
        self.__notifications.remove(notification)
        self.__rearrange_notifications()

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

    @classmethod
    def __get_icon_pixmaps(cls):
        app = QApplication.instance() or QApplication([])
        style = app.style()

        information_icon = style.standardIcon(QStyle.SP_MessageBoxInformation)
        sizes = information_icon.availableSizes()
        cls.__icons["INFORMATION_ICON_16x16"] = information_icon.pixmap(sizes[0])
        cls.__icons["INFORMATION_ICON_32x32"] = information_icon.pixmap(sizes[1])

        warning_icon = style.standardIcon(QStyle.SP_MessageBoxWarning)
        sizes = warning_icon.availableSizes()
        cls.__icons["WARNING_ICON_16x16"] = warning_icon.pixmap(sizes[0])
        cls.__icons["WARNING_ICON_32x32"] = warning_icon.pixmap(sizes[1])

        critical_icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        sizes = critical_icon.availableSizes()
        cls.__icons["CRITICAL_ICON_16x16"] = critical_icon.pixmap(sizes[0])
        cls.__icons["CRITICAL_ICON_32x32"] = critical_icon.pixmap(sizes[1])

        question_icon = style.standardIcon(QStyle.SP_MessageBoxQuestion)
        sizes = question_icon.availableSizes()
        cls.__icons["QUESTION_ICON_16x16"] = question_icon.pixmap(sizes[0])
        cls.__icons["QUESTION_ICON_32x32"] = question_icon.pixmap(sizes[1])
