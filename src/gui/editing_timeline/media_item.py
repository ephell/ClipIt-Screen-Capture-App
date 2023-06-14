from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaItem(QGraphicsWidget):

    def __init__(self):
        super().__init__()
        self.pen = QPen(Qt.red, 3)
        self.rect = self.boundingRect()

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, 750, 100)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(self.pen)
        painter.drawRect(self.boundingRect())
