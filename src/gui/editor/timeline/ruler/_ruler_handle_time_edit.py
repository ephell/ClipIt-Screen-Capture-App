from PySide6.QtCore import Signal, Slot, QTime
from PySide6.QtWidgets import QGraphicsProxyWidget, QTimeEdit


class RulerHandleTimeEdit(QTimeEdit):

    time_changed_via_ui_signal = Signal(int)
    time_changed_via_code_signal = Signal(int)

    def __init__(self, scene, media_duration):
        super().__init__(None)
        self.scene = scene
        self.__proxy = QGraphicsProxyWidget()
        self.__proxy.setWidget(self)
        self.__proxy.setPos(28, 129)
        self.__proxy.setFlag(QGraphicsProxyWidget.ItemIsFocusable, True)
        self.scene.addItem(self.__proxy)
        self.setDisplayFormat("mm:ss:zzz")
        self.setMinimumTime(QTime(0, 0, 0, 0))
        self.setMaximumTime(QTime(0, 0, 0, 0).addMSecs(media_duration))
        self.setWrapping(True)
        self.timeChanged.connect(self.__on_time_changed)

    """Override"""
    def stepBy(self, steps):
        if self.__get_time_in_ms() + steps >= self.__get_maximum_time_ms():
            self.__set_time_in_ms(self.__get_maximum_time_ms())
        elif self.__get_time_in_ms() + steps <= self.__get_minimum_time_ms():
            self.__set_time_in_ms(self.__get_minimum_time_ms())
        else:
            self.__set_time_in_ms(self.__get_time_in_ms() + steps)

    @Slot()
    def __on_time_changed(self):
        """
        Have to send separate signals because if they're combined into
        one, the 'on_ruler_handle_time_changed()' slot in the MediaItem
        class gets called unnecessarily when the time is changed via code
        (not manually by typing in the time). It makes the video and audio 
        playback in MediaPlayer stutter.
        """
        if self.hasFocus():
            self.time_changed_via_ui_signal.emit(self.__get_time_in_ms())
        else:
            self.time_changed_via_code_signal.emit(self.__get_time_in_ms())
        
    def update_time(self, time_ms):
        self.__set_time_in_ms(time_ms)

    def get_time(self):
        return self.__get_time_in_ms()

    def __get_minimum_time_ms(self):
        min_time = self.minimumTime()
        minutes = min_time.minute()
        seconds = min_time.second()
        milliseconds = min_time.msec()
        return milliseconds + (seconds * 1000) + (minutes * 60 * 1000)

    def __get_maximum_time_ms(self):
        max_time = self.maximumTime()
        minutes = max_time.minute()
        seconds = max_time.second()
        milliseconds = max_time.msec()
        return milliseconds + (seconds * 1000) + (minutes * 60 * 1000)

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
