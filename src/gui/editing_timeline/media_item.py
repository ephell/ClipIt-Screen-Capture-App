from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MediaItem(QGraphicsWidget):

    def __init__(self):
        super().__init__()
        self.pen = QPen(Qt.red, 3)
        self.resize_handle_width = 10
        self.resizing = False
        self.is_first_paint = True 
        self.width = 0
        self.height = 100

    """Override"""
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        if self.is_first_paint:
            self.is_first_paint = False
            self.width = int(self.scene().width() - self.pos().x() * 2)
            self.setMaximumWidth(self.width)
            self.setMinimumWidth(50)
            self.resize(self.width, self.height)

        if self.resizing:
            resize_handle_rect = self.resize_handle_rect()
            painter.fillRect(resize_handle_rect, Qt.black)

        painter.setPen(self.pen)
        painter.drawRect(self.boundingRect())

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    """Override"""
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            resize_handle_rect = self.resize_handle_rect()
            if resize_handle_rect.contains(event.pos()):
                self.resizing = True
                self.setCursor(Qt.SplitHCursor)
                event.accept()

    """Override"""
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.resizing:
            new_width = event.scenePos().x() - self.scenePos().x()
            new_width = max(new_width, self.minimumWidth())
            new_width = min(new_width, self.maximumWidth())
            self.width = new_width
            self.prepareGeometryChange()
            self.update()

    """Override"""
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self.resizing:
            self.resizing = False
            self.setCursor(Qt.ArrowCursor)
            self.update()

    def resize_handle_rect(self):
        rect = self.boundingRect()
        return QRectF(
            rect.right() - self.resize_handle_width, 
            rect.top(), 
            self.resize_handle_width, 
            rect.height()
        )
