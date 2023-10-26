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
        self.notifications = []
        if any(icon is None for icon in self.__icons.values()):
            self.__get_icon_pixmaps()

    def send_information(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["INFORMATION_ICON_32x32"])

    def send_warning(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["WARNING_ICON_32x32"])

    def send_critical(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["CRITICAL_ICON_32x32"])

    def send_question(self, message, time_ms):
        self.__send_notification(message, time_ms, self.__icons["QUESTION_ICON_32x32"])

    def __send_notification(self, message, time_ms, icon):
        notification = Notification(message, time_ms, icon)
        notification.closed_signal.connect(lambda: self.notifications.remove(notification))
        self.notifications.append(notification)

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
