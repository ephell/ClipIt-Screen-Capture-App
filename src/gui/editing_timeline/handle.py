from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RulerHandle(QGraphicsWidget):
    
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.setPos(30, 0)
        self.brush = QBrush(Qt.magenta)
        self.pen = QPen(Qt.magenta)
        self.rect = self.boundingRect()
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsWidget.ItemIsSelectable, True)

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, 1, 100)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawRect(self.boundingRect())

    """Override"""
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Restrict movement to X-axis only
            value.setY(self.pos().y())
        return super().itemChange(change, value)
    
    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path
