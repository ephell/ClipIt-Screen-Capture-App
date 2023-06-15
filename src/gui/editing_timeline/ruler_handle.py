from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RulerHandle(QGraphicsItem):
    
    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.time_label = _RulerHandleTimeLabel(self)
        self.maximum_possible_duration = media_duration
        self.width = 30
        self.height = 100 + self.scene.media_item_y - self.scene.ruler_handle_y
        self.head_width = self.width
        self.head_height = self.height / 10
        self.needle_width = 1
        self.needle_height = self.height - self.head_height
        self.needle_x = (self.width - self.needle_width) / 2
        self.needle_y = self.head_height
        self.minimum_x = self.scene.ruler_handle_x - self.width / 2
        self.maximum_x = self.scene.width() - self.width * 2 + self.minimum_x
        self.setPos(self.minimum_x, self.scene.ruler_handle_y)

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
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            current_x = value.x()
            delta_x = current_x - self.pos().x()
            if current_x < self.minimum_x:
                new_pos = QPointF(self.minimum_x, self.pos().y())
            elif current_x > self.maximum_x:
                new_pos = QPointF(self.maximum_x, self.pos().y())
            else:
                new_pos = QPointF(value.x(), self.pos().y())
            self.__update_time_label(delta_x)
            return new_pos
        return super().itemChange(change, value)
    
    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, self.head_width, self.head_height)
        return path
    
    def __update_time_label(self, delta_x):
        new_timestamp = self.__calculate_duration(delta_x)
        formatted_timestamp = self.__format_duration(new_timestamp)
        self.time_label.setPlainText(formatted_timestamp)
        return new_timestamp

    def __calculate_duration(self, delta_x=0):
        handle_range = self.maximum_x - self.minimum_x
        handle_position = self.pos().x() - self.minimum_x + delta_x
        time_ratio = handle_position / handle_range
        new_duration = time_ratio * self.maximum_possible_duration
        if new_duration > self.maximum_possible_duration:
            new_duration = self.maximum_possible_duration
        elif new_duration < 0:
            new_duration = 0
        return new_duration
    
    def __format_duration(self, duration):
        milliseconds = int(duration)
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}:{milliseconds:02d}"


class _RulerHandleTimeLabel(QGraphicsTextItem):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(10, 160)
        font = self.font()
        font.setPointSize(15)
        font.setWeight(QFont.Bold)
        self.setFont(font)
