from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RulerHandle(QGraphicsWidget):
    
    def __init__(self):
        super().__init__()
        self.rect_brush = QBrush(Qt.blue)
        self.rect_pen = QPen(Qt.blue)
        self.rect = self.boundingRect()
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsWidget.ItemIsSelectable, True)

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, 5, 100)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setBrush(self.rect_brush)
        painter.setPen(self.rect_pen)
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
