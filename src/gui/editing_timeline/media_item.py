from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .media_item_left_handle import LeftHandle
from .media_item_right_handle import RightHandle


class MediaItem(QGraphicsRectItem):

    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.media_duration = media_duration
        self.start_time = 0
        self.end_time = media_duration
        self.initial_x = self.scene.media_item_x
        self.initial_y = self.scene.media_item_y
        self.setPos(self.initial_x, self.initial_y)
        self.initial_width = self.calculate_width_from_time_interval(
            self.start_time, self.end_time
        )
        self.initial_height = 100
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
        self.resize_based_on_time_interval(self.start_time, self.end_time)
        self.move_to_x_based_on_time(self.start_time)
        self.left_handle.update_position()
        self.right_handle.update_position()
        self.update()

    def calculate_max_possible_width(self):
        return int(self.scene.width() - self.initial_x * 2)

    def calculate_width_from_time_interval(self, start_time, end_time):
        total_time = self.media_duration
        max_possible_width = self.calculate_max_possible_width()
        return (end_time - start_time) / total_time * max_possible_width
    
    def calculate_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.calculate_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def calculate_time_from_x_pos(self, x_pos):
        total_time = self.media_duration
        max_possible_width = self.calculate_max_possible_width()
        return (x_pos - self.initial_x) / max_possible_width * total_time

    def move_to_x_based_on_time(self, time):
        self.setPos(self.calculate_x_pos_from_time(time), self.initial_y)

    def resize_based_on_time_interval(self, start_time, end_time):
        self.setRect(
            0, 
            0,
            self.calculate_width_from_time_interval(start_time, end_time), 
            self.initial_height
        )

    def update_start_time(self, time):
        self.start_time = time
        self.time_label.update_start_time(time)

    def update_end_time(self, time):
        self.end_time = time
        self.time_label.update_end_time(time)


class _TimeLabel(QGraphicsTextItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(
            self.parent.scene.media_item_x + 485, 
            self.parent.scene.media_item_y + 105
        )
        font = self.font()
        font.setPointSize(15)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        self.start_time = self.format_timestamp(self.parent.start_time)
        self.end_time = self.format_timestamp(self.parent.end_time)
        self.__update_label()

    def update_start_time(self, timestamp):
        self.start_time = self.format_timestamp(timestamp)
        self.__update_label()

    def update_end_time(self, timestamp):
        self.end_time = self.format_timestamp(timestamp)
        self.__update_label()

    def __update_label(self):
        self.setPlainText(f"{self.start_time} to {self.end_time}")

    @staticmethod
    def format_timestamp(time):
        """Formats a timestamp in milliseconds to a string."""
        milliseconds = int(time)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
