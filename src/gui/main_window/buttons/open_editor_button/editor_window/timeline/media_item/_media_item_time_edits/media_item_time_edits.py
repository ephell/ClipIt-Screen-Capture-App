from PySide6.QtCore import Qt, QTime, Slot, Signal
from PySide6.QtWidgets import QWidget, QGraphicsProxyWidget

from .Ui_MediaItemTimeEdits import Ui_MediaItemTimeEdits


class TimeEdits(QWidget, Ui_MediaItemTimeEdits):

    left_handle_time_edit_time_changed_signal = Signal(int)
    right_handle_time_edit_time_changed_signal = Signal(int)

    def __init__(self, scene, media_duration):
        super().__init__(None)
        self.scene = scene
        self.media_duration = media_duration
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.__proxy = QGraphicsProxyWidget()
        self.__proxy.setWidget(self)
        self.__proxy.setPos(
            self.scene.width() - 197,
            self.scene.sceneRect().y() + 116
        )
        self.scene.addItem(self.__proxy)
        # Setting display format in their respective classes doesn't work
        # in this case for some reason.
        self.left_handle_time_edit.setDisplayFormat("mm:ss:zzz")
        self.right_handle_time_edit.setDisplayFormat("mm:ss:zzz")
        self.__connect_signals_and_slots()
        self.__set_initial_times()

    def __connect_signals_and_slots(self):
        self.left_handle_time_edit.time_changed_signal.connect(
            self.__on_left_handle_time_changed
        )
        self.right_handle_time_edit.time_changed_signal.connect(
            self.__on_right_handle_time_changed
        )

    @Slot()
    def __on_left_handle_time_changed(self, time_ms):
        if self.right_handle_time_edit.get_time() <= time_ms:
            self.right_handle_time_edit.update_time(time_ms + 1)
        self.left_handle_time_edit_time_changed_signal.emit(time_ms)
        
    @Slot()
    def __on_right_handle_time_changed(self, time_ms):
        if self.left_handle_time_edit.get_time() >= time_ms:
            self.left_handle_time_edit.update_time(time_ms - 1)
        self.right_handle_time_edit_time_changed_signal.emit(time_ms)

    def update_start_time(self, new_time_ms):
        self.left_handle_time_edit.update_time(new_time_ms)

    def update_end_time(self, new_time_ms):
        self.right_handle_time_edit.update_time(new_time_ms)

    def on_view_resize(self):
        """Set new position when graphics view is resized."""
        self.__proxy.setPos(
            self.scene.width() - 197,
            self.scene.sceneRect().y() + 116
        )

    def __set_initial_times(self):
        self.left_handle_time_edit.update_time(0)
        self.right_handle_time_edit.update_time(self.media_duration)
        self.left_handle_time_edit.setMinimumTime(
            QTime(0, 0, 0, 0)
        )
        self.left_handle_time_edit.setMaximumTime(
            QTime(0, 0, 0, 0).addMSecs(self.media_duration - 1)
        )
        self.right_handle_time_edit.setMinimumTime(
            QTime(0, 0, 0, 0).addMSecs(1)
        )
        self.right_handle_time_edit.setMaximumTime(
            QTime(0, 0, 0, 0).addMSecs(self.media_duration)
        )
