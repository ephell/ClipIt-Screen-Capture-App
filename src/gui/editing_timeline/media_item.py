from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .time_utils import TimeUtils


class MediaItem(QGraphicsRectItem):

    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.setPos(self.scene.media_item_x, self.scene.media_item_y)
        self.setRect(QRectF(0, 0, self.scene.width() - self.pos().x() * 2, 100))
        self.setPen(QPen(Qt.blue, 1))
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.original_width = self.rect().width()
        self.minimum_width = 1
        self.media_duration = media_duration
        self.maximum_possible_duration = media_duration
        self.right_handle = _RightHandle(self)
        self.left_handle = _LeftHandle(self)
        self.time_label = _TimeLabel(self)


class _RightHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setRect(0, 0, 15, self.parent.rect().height())
        self.setPen(QPen(Qt.red, 1))
        self.setPos(parent.pos().x() + parent.rect().width(), parent.pos().y())
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.minimum_x = self.parent.pos().x()
        self.maximum_x = self.parent.pos().x() + self.parent.original_width

    """Override"""
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            delta_x = value.x() - self.pos().x()
            new_width = self.parent.rect().width() + delta_x
            available_width = \
                self.parent.original_width - (new_width + self.parent.rect().x())
            if (new_width <= self.parent.original_width) \
                    and (available_width >= 0) \
                    and (new_width >= self.parent.minimum_width):
                self.parent.setRect(
                    self.parent.rect().x(), 
                    self.parent.rect().y(),
                    new_width,
                    self.parent.rect().height()
                )
                timestamp = TimeUtils.calculate_timestamp_by_handle_position(
                    delta_x,
                    self.pos().x(),
                    self.maximum_x,
                    self.minimum_x,
                    self.parent.maximum_possible_duration
                )
                timestamp = TimeUtils.format_timestamp(timestamp)
                self.parent.time_label.update_right_handle_timestamp(timestamp)
                return QPointF(value.x(), self.parent.pos().y())
            return QPointF(self.pos().x(), self.parent.pos().y())
        return super().itemChange(change, value)
    

class _LeftHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setRect(0, 0, 15, self.parent.rect().height())
        self.setPen(QPen(Qt.red, 1))
        self.setPos(parent.pos().x() - self.rect().width(), parent.pos().y())
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.minimum_x = self.parent.pos().x() - self.rect().width()
        self.maximum_x = self.minimum_x + self.parent.original_width
        
    """Override"""
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            delta_x = value.x() - self.pos().x()
            new_width = self.parent.rect().width() - delta_x
            if (self.parent.rect().x() + delta_x >= 0) \
                    and (new_width >= self.parent.minimum_width):
                self.parent.setRect(
                    self.parent.rect().x() + delta_x, 
                    self.parent.rect().y(), 
                    new_width, 
                    self.parent.rect().height()
                )
                timestamp = TimeUtils.calculate_timestamp_by_handle_position(
                    delta_x,
                    self.pos().x(),
                    self.maximum_x,
                    self.minimum_x,
                    self.parent.maximum_possible_duration
                )
                timestamp = TimeUtils.format_timestamp(timestamp)
                self.parent.time_label.update_left_handle_timestamp(timestamp)
                return QPointF(value.x(), self.parent.pos().y())
            return QPointF(self.pos().x(), self.parent.pos().y())
        return super().itemChange(change, value)


class _TimeLabel(QGraphicsTextItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(
            self.parent.scene.media_item_x + 535, 
            self.parent.scene.media_item_y + 105
        )
        font = self.font()
        font.setPointSize(15)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        self.left_handle_timestamp = "00:00:000"
        self.right_handle_timestamp = "00:00:000"
        self.__update_label()

    def update_left_handle_timestamp(self, timestamp):
        self.left_handle_timestamp = timestamp
        self.__update_label()

    def update_right_handle_timestamp(self, timestamp):
        self.right_handle_timestamp = timestamp
        self.__update_label()

    def __update_label(self):
        self.setPlainText(
            f"{self.left_handle_timestamp} to {self.right_handle_timestamp}"
        )
