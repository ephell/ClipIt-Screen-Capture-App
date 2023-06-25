from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RulerHandle(QGraphicsItem):
    
    def __init__(self, ruler, media_duration):
        super().__init__()
        self.ruler = ruler
        self.scene = self.ruler.scene
        self.scene.addItem(self)
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.media_duration = media_duration
        self.width = 10
        self.height = 100 + self.scene.media_item_y
        self.left_pad_x = self.scene.ruler_x
        self.right_pad_x = self.scene.ruler_x
        self.top_pad_y = 0
        self.initial_x = self.__get_min_possible_x()
        self.initial_y = self.top_pad_y
        self.setPos(self.initial_x, self.initial_y)
        self.head_width = self.width
        self.head_height = self.height / 15
        self.needle_width = 1
        self.needle_height = self.height - self.head_height
        self.needle_x = (self.width - self.needle_width) / 2
        self.needle_y = self.head_height
        self.time_label = _RulerHandleTimeLabel(self)

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.magenta))
        painter.setBrush(QBrush(Qt.magenta))
        painter.drawRect(QRectF(0, 0, self.head_width, self.head_height))
        painter.drawRect(QRectF(
            self.needle_x, self.needle_y, self.needle_width, self.needle_height
        ))

    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, self.head_width, self.head_height)
        return path

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    """Override"""
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.__move(event.scenePos())

    @Slot()
    def on_media_player_position_changed(self, time):
        self.setPos(
            self.__get_x_pos_from_time(time), 
            self.scenePos().y()
        )   
        self.time_label.update_label(time)

    @Slot()
    def on_media_item_left_handle_moved(self, time):
        if time > self.time_label.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_label.update_label(time)
            self.scene.ruler_handle_time_changed.emit(time)

    @Slot()
    def on_media_item_right_handle_moved(self, time):
        if time < self.time_label.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_label.update_label(time)
            self.scene.ruler_handle_time_changed.emit(time)

    def on_view_resize(self):
        """Not a slot. Called in 'Ruler' object."""
        self.setPos(
            self.__get_x_pos_from_time(self.time_label.get_time()), 
            self.scenePos().y()
        )

    def on_ruler_left_mouse_clicked(self, click_pos):
        """Not a slot. Called in 'Ruler' object."""
        self.__move(click_pos)

    def __move(self, position):
        new_x = position.x() - self.width / 2
        if new_x <= self.__get_min_possible_x():
            new_x = self.__get_min_possible_x()
        elif new_x >= self.__get_max_possible_x():
            new_x = self.__get_max_possible_x()
        self.setPos(new_x, self.scenePos().y())
        self.time_label.update_label(self.__get_current_time())
        self.scene.ruler_handle_time_changed.emit(self.__get_current_time())

    def __get_max_possible_width(self):
        return self.scene.width() - self.left_pad_x - self.right_pad_x

    def __get_min_possible_x(self):
        return self.left_pad_x - self.width / 2

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()
    
    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()
    
    def __get_current_time(self):
        current_position = self.scenePos().x() - self.__get_min_possible_x()
        return self.__convert_pixels_to_time(current_position)
    
    def __get_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())


class _RulerHandleTimeLabel(QGraphicsTextItem):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(
            self.parent.scene.sceneRect().x() + 23,
            self.parent.scene.sceneRect().y() + 160
        )
        font = self.font()
        font.setPointSize(15)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        self.time = 0
        self.timestamp = ""
        self.update_label(0)

    def update_label(self, time):
        self.time = time
        self.timestamp = self.format_time(time)
        self.setPlainText(self.timestamp)

    def get_time(self):
        return self.time

    @staticmethod
    def format_time(time):
        """Formats a time in milliseconds to a string."""
        milliseconds = int(time)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
