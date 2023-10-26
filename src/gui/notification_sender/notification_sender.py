from PySide6.QtCore import QTimer

from ._notification_widget import Notification


class NotificationSender:

    def __init__(self):
        self.notifications = []

    def send_notification(self, message, time_ms):
        notification = Notification(message)
        notification.show()
        QTimer.singleShot(time_ms, notification.close)
        self.notifications.append(notification)
