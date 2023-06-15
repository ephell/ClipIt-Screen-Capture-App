from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RulerHandle(QGraphicsItem):
    
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.width = 30
        self.height = 100 + self.scene.media_item_y - self.scene.ruler_handle_y
        self.rect = self.boundingRect()

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
            if current_x < self.minimum_x:
                return QPointF(self.minimum_x, self.pos().y())
            elif current_x > self.maximum_x:
                return QPointF(self.maximum_x, self.pos().y())
            return QPointF(value.x(), self.pos().y())
        return super().itemChange(change, value)
    
    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, self.head_width, self.head_height)
        return path
