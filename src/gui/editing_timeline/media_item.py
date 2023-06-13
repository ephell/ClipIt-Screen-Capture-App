from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaItem(QGraphicsWidget):
    
    def __init__(self):
        super().__init__()
        self.rect_brush = QBrush(Qt.red)
        self.rect_pen = QPen(Qt.red, 3)
        self.rect = self.boundingRect()

    def boundingRect(self):
        return QRectF(0, 0, 750, 100)

    def paint(self, painter, option, widget):
        # painter.setBrush(self.rect_brush)
        painter.setPen(self.rect_pen)
        painter.drawRect(self.boundingRect())
