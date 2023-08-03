from PySide6.QtCore import Signal, Slot, QTime
from PySide6.QtWidgets import QGraphicsProxyWidget, QTimeEdit


class RulerHandleTimeEdit(QTimeEdit):

    time_changed_signal = Signal(int)

    def __init__(self, scene, media_duration):
        super().__init__(None)
        self.scene = scene
        self.__proxy = QGraphicsProxyWidget()
        self.__proxy.setWidget(self)
        self.__proxy.setPos(28, 129)
        self.scene.addItem(self.__proxy)
        self.setDisplayFormat("mm:ss:zzz")
        self.setMinimumTime(QTime(0, 0, 0, 0))
        self.setMaximumTime(QTime(0, 0, 0, 0).addMSecs(media_duration))
        self.setWrapping(True)
        self.timeChanged.connect(self.__on_time_changed)

    """Override"""
    def stepBy(self, steps):
        self.__set_time_in_ms(self.__get_time_in_ms() + steps)

    @Slot()
    def __on_time_changed(self):
        self.time_changed_signal.emit(self.__get_time_in_ms())

    def update_time(self, time_ms):
        self.__set_time_in_ms(time_ms)

    def get_time(self):
        return self.__get_time_in_ms()

    def __get_time_in_ms(self):
        time = self.time()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec()
        return milliseconds + (seconds * 1000) + (minutes * 60 * 1000)

    def __set_time_in_ms(self, time_ms):
        seconds, milliseconds = divmod(int(time_ms), 1000)
        minutes, seconds = divmod(seconds, 60)
        self.setTime(QTime(0, minutes, seconds, milliseconds))
