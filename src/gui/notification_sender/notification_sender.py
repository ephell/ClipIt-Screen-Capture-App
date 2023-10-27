from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QStyle

from ._notification_widget import Notification


def get_icon_pixmaps(cls):
    if any(icon is None for icon in cls.icon_pixmaps.values()):
        cls.get_icon_pixmaps()
    return cls


@get_icon_pixmaps
class NotificationSender:

    icon_pixmaps = {
        'INFORMATION_ICON_16x16': None,
        'INFORMATION_ICON_32x32': None,
        'WARNING_ICON_16x16': None,
        'WARNING_ICON_32x32': None,
        'CRITICAL_ICON_16x16': None,
        'CRITICAL_ICON_32x32': None,
        'QUESTION_ICON_16x16': None,
        'QUESTION_ICON_32x32': None,
    }

    __notifications = []
    __app = QApplication.instance() or QApplication([])
    __x_padding = 25
    __y_padding = 0

    @classmethod
    def get_icon_pixmaps(cls):
        app = QApplication.instance() or QApplication([])
        style = app.style()

        information_icon = style.standardIcon(QStyle.SP_MessageBoxInformation)
        sizes = information_icon.availableSizes()
        cls.icon_pixmaps["INFORMATION_ICON_16x16"] = information_icon.pixmap(sizes[0])
        cls.icon_pixmaps["INFORMATION_ICON_32x32"] = information_icon.pixmap(sizes[1])

        warning_icon = style.standardIcon(QStyle.SP_MessageBoxWarning)
        sizes = warning_icon.availableSizes()
        cls.icon_pixmaps["WARNING_ICON_16x16"] = warning_icon.pixmap(sizes[0])
        cls.icon_pixmaps["WARNING_ICON_32x32"] = warning_icon.pixmap(sizes[1])

        critical_icon = style.standardIcon(QStyle.SP_MessageBoxCritical)
        sizes = critical_icon.availableSizes()
        cls.icon_pixmaps["CRITICAL_ICON_16x16"] = critical_icon.pixmap(sizes[0])
        cls.icon_pixmaps["CRITICAL_ICON_32x32"] = critical_icon.pixmap(sizes[1])

        question_icon = style.standardIcon(QStyle.SP_MessageBoxQuestion)
        sizes = question_icon.availableSizes()
        cls.icon_pixmaps["QUESTION_ICON_16x16"] = question_icon.pixmap(sizes[0])
        cls.icon_pixmaps["QUESTION_ICON_32x32"] = question_icon.pixmap(sizes[1])

    @classmethod
    def send_information(cls, message, time_ms):
        cls.__send_notification(message, time_ms, cls.icon_pixmaps["INFORMATION_ICON_16x16"])

    @classmethod
    def send_warning(cls, message, time_ms):
        cls.__send_notification(message, time_ms, cls.icon_pixmaps["WARNING_ICON_16x16"])

    @classmethod
    def send_critical(cls, message, time_ms):
        cls.__send_notification(message, time_ms, cls.icon_pixmaps["CRITICAL_ICON_16x16"])

    @classmethod
    def send_question(cls, message, time_ms):
        cls.__send_notification(message, time_ms, cls.icon_pixmaps["QUESTION_ICON_16x16"])

    @classmethod
    def __send_notification(cls, message, time_ms, icon):
        last_notification = cls.__notifications[-1] if cls.__notifications else None
        new_notification = Notification(message, time_ms, icon)
        new_notification.set_position(
            *cls.__calculate_position(
                new_notification,
                last_notification
            )
        )
        new_notification.closed_signal.connect(
            lambda notification: cls.__on_notification_closed(cls, notification)
        )
        cls.__notifications.append(new_notification)
        new_notification.show()

    @Slot()
    def __on_notification_closed(cls, notification):
        cls.__notifications.remove(notification)
        cls.__rearrange_notifications()

    @classmethod
    def __calculate_position(cls, new_notification, last_notification):
        if last_notification is None:
            return cls.__calculate_bottom_most_position(new_notification)

        last_notification_x = last_notification.x()
        last_notification_y = last_notification.y()
        new_notification_h = new_notification.height()
        _, screen_size_diff_h = cls.__get_screen_size_difference()
        return (
            last_notification_x,
            last_notification_y - new_notification_h - cls.__y_padding - screen_size_diff_h
        )

    @classmethod
    def __calculate_bottom_most_position(cls, notification):
        available_w, available_h = cls.__get_available_screen_size()
        size_diff_w, size_diff_h = cls.__get_screen_size_difference()
        return (
            available_w - notification.width() - size_diff_w - cls.__x_padding,
            available_h - notification.height() - size_diff_h - cls.__y_padding
        )

    @classmethod
    def __rearrange_notifications(cls):
        for i, notification in enumerate(cls.__notifications):
            if i == 0:
                notification.set_position(
                    *cls.__calculate_bottom_most_position(notification)
                )
            else:
                last_notification = cls.__notifications[i-1]
                notification.set_position(
                    *cls.__calculate_position(
                        notification,
                        last_notification
                    )
                )

    @classmethod
    def __get_available_screen_size(cls):
        return cls.__app.primaryScreen().availableSize().toTuple()

    @classmethod
    def __get_total_screen_size(cls):
        return cls.__app.primaryScreen().size().toTuple()

    @classmethod
    def __get_screen_size_difference(cls):
        total_w, total_h = cls.__get_total_screen_size()
        available_w, available_h = cls.__get_available_screen_size()
        return total_w - available_w, total_h - available_h
