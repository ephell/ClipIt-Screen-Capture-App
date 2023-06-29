from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from ._media_item_left_handle import LeftHandle
from ._media_item_right_handle import RightHandle


class MediaItem(QGraphicsRectItem):

    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.media_duration = media_duration
        self.start_time = 0
        self.end_time = media_duration
        self.left_pad_x = self.scene.media_item_x
        self.right_pad_x = self.scene.media_item_x
        self.top_pad_y = self.scene.media_item_y
        self.initial_x = self.left_pad_x
        self.initial_y = self.top_pad_y
        self.setPos(self.initial_x, self.initial_y)
        self.initial_width = self.__get_width_from_time_interval(
            self.start_time, self.end_time
        )
        self.initial_height = 70
        self.setRect(0, 0, self.initial_width, self.initial_height)
        self.left_handle = LeftHandle(self)
        self.right_handle = RightHandle(self)
        self.time_label = _TimeLabel(self)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.blue, 1))
        painter.drawRect(self.boundingRect())

    @Slot()
    def on_view_resize(self):
        self.__resize_based_on_time_interval(self.start_time, self.end_time)
        self.__move_to_x_based_on_time(self.start_time)
        self.left_handle.setPos(
            self.scenePos().x() - self.left_handle.handle_width,
            self.scenePos().y()
        )
        self.right_handle.setPos(
            self.scenePos().x() + self.rect().width(),
            self.scenePos().y()
        )
        self.time_label.on_view_resize()
        self.update()

    @Slot()
    def on_ruler_handle_time_changed(self, time):
        if time < self.start_time:
            self.update_start_time(time)
            self.__resize_based_on_time_interval(time, self.end_time)
            self.__move_to_x_based_on_time(time)
            self.left_handle.setPos(
                self.scenePos().x() - self.left_handle.handle_width,
                self.scenePos().y()
            )
        elif time > self.end_time:
            self.update_end_time(time)
            self.__resize_based_on_time_interval(self.start_time, time)
            self.right_handle.setPos(
                self.scenePos().x() + self.rect().width(),
                self.scenePos().y()
            )

    def update_start_time(self, time):
        self.start_time = time
        self.time_label.update_start_time(time)
        self.scene.media_item_start_time_changed.emit(time)

    def update_end_time(self, time):
        self.end_time = time
        self.time_label.update_end_time(time)
        self.scene.media_item_end_time_changed.emit(time)

    def __get_max_possible_width(self):
        return self.scene.width() - self.left_pad_x - self.right_pad_x
    
    def __get_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def __move_to_x_based_on_time(self, time):
        self.setPos(self.__get_x_pos_from_time(time), self.initial_y)

    def __get_width_from_time_interval(self, start_time, end_time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (end_time - start_time) / total_time * max_possible_width

    def __resize_based_on_time_interval(self, start_time, end_time):
        self.setRect(
            0, 
            0,
            self.__get_width_from_time_interval(start_time, end_time), 
            self.initial_height
        )


class _TimeLabel(QGraphicsTextItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(
            self.parent.scene.width() - 257,
            self.parent.scene.sceneRect().y() + 120
        )
        font = self.font()
        font.setPointSize(16)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        self.start_time = self.format_time(self.parent.start_time)
        self.end_time = self.format_time(self.parent.end_time)
        self.__update_label()

    def update_start_time(self, time):
        self.start_time = self.format_time(time)
        self.__update_label()

    def update_end_time(self, time):
        self.end_time = self.format_time(time)
        self.__update_label()

    def on_view_resize(self):
        self.setPos(
            self.parent.scene.width() - 257,
            self.parent.scene.sceneRect().y() + 120
        )

    def __update_label(self):
        self.setPlainText(f"{self.start_time} to {self.end_time}")

    @staticmethod
    def format_time(time):
        """Formats a time in milliseconds to a string."""
        milliseconds = int(time)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
