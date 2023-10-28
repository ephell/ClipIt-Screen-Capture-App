from PySide6.QtCore import Slot

from ._notification_manager import NotificationManager


class NotificationSender:

    __instance = None

    def __new__(self):
        if self.__instance is None:
            self.__instance = super().__new__(self)
            self.__instance.__init()
        return self.__instance

    def __init(self):
        self.__manager = NotificationManager()
        self.__manager.ready_to_display_signal.connect(self.__on_ready_to_display)
        self.__manager.start()

    def send(self, message, time_ms, type="information", image=None):
        self.__manager.put_in_queue(message, time_ms, type, image)

    @Slot()
    def __on_ready_to_display(self, notification):
        notification.show()
