from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .time_utils import TimeUtils


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
            new_x = value.x()
            delta_x = new_x - self.pos().x()
            if new_x < self.minimum_x:
                new_pos = QPointF(self.minimum_x, self.pos().y())
            elif new_x > self.maximum_x:
                new_pos = QPointF(self.maximum_x, self.pos().y())
            else:
                new_pos = QPointF(new_x, self.pos().y())
            timestamp = TimeUtils.calculate_timestamp_by_handle_position(
                delta_x,
                self.pos().x(),
                self.maximum_x,
                self.minimum_x,
                self.maximum_possible_duration
            )
            timestamp = TimeUtils.format_timestamp(timestamp)
            self.time_label.update_label(timestamp)
            return new_pos
        return super().itemChange(change, value)
    
    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, self.head_width, self.head_height)
        return path

class _RulerHandleTimeLabel(QGraphicsTextItem):
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setPos(
            self.parent.scene.media_item_x - 20,
            self.parent.scene.media_item_y + 105
        )
        font = self.font()
        font.setPointSize(15)
        font.setWeight(QFont.Bold)
        self.setFont(font)
        self.timestamp = "00:00:000"

    def update_label(self, timestamp):
        self.timestamp = timestamp
        self.setPlainText(self.timestamp)
