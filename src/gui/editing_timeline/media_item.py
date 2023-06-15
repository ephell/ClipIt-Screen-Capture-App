from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MediaItem(QGraphicsWidget):

    def __init__(self, media_duration):
        super().__init__()
        self.media_duration = media_duration
        self.maximum_media_duration = media_duration
        self.resizing = False
        self.resizing_right = False
        self.resizing_left = False
        self.is_first_paint = True 
        self.width = 0
        self.height = 100
        self.right_resize_handle = 10
        self.left_resize_handle = 10
        self.minimum_width = 1
        self.maximum_x = 0
        self.minimum_x = 0

    """Override"""
    def paint(self, painter, option, widget):
        super().paint(painter, option, widget)

        if self.is_first_paint:
            self.is_first_paint = False
            self.width = int(self.scene().width() - self.pos().x() * 2)
            self.resize(self.width, self.height)
            self.setMaximumWidth(self.width)
            self.setMinimumWidth(self.minimum_width)
            self.maximum_x = self.width + self.pos().x()
            self.minimum_x = self.pos().x()

        painter.setPen(QPen(Qt.red, 1))
        painter.drawRect(self.boundingRect())

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    """Override"""
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            right_resize_handle_rect = self.right_resize_handle_rect()
            left_resize_handle_rect = self.left_resize_handle_rect()
            if right_resize_handle_rect.contains(event.pos()):
                self.resizing = self.resizing_right = True
                self.setCursor(Qt.SplitHCursor)
                event.accept()
            elif left_resize_handle_rect.contains(event.pos()):
                self.resizing = self.resizing_left = True
                self.setCursor(Qt.SplitHCursor)
                event.accept()

    """Override"""
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.resizing:
            if self.resizing_right:
                new_width = event.scenePos().x() - self.scenePos().x()
                new_width = max(new_width, self.minimumWidth())
                new_width = min(new_width, self.maximumWidth())

                new_x = self.scenePos().x()
                if new_x + new_width > self.maximum_x:
                    new_width = self.maximum_x - new_x
                self.width = new_width

            elif self.resizing_left:
                current_x = max(event.scenePos().x(), self.minimum_x)
                amount_resized = current_x - self.scenePos().x()
                new_width = self.boundingRect().width() - amount_resized
                new_width = max(new_width, self.minimumWidth())
                new_width = min(new_width, self.maximumWidth())

                new_x = self.scenePos().x() + amount_resized
                if new_x < self.minimum_x:
                    new_x = self.minimum_x
                elif new_x > self.maximum_x:
                    new_x = self.maximum_x - new_width

                self.setPos(new_x, self.scenePos().y())
                self.width = new_width

            self.prepareGeometryChange()
            self.update()
            self.resize_duration()

    """Override"""
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.resizing = self.resizing_right = self.resizing_left = False
            self.setCursor(Qt.ArrowCursor)
            self.update()

    def right_resize_handle_rect(self):
        rect = self.boundingRect()
        return QRectF(
            rect.right() - self.right_resize_handle, 
            rect.top(), 
            self.right_resize_handle, 
            rect.height()
        )
    
    def left_resize_handle_rect(self):
        rect = self.boundingRect()
        return QRectF(
            rect.left(), 
            rect.top(), 
            self.left_resize_handle, 
            rect.height()
        )

    def resize_duration(self):
        duration_ratio = self.width / self.maximumWidth()
        new_duration = duration_ratio * self.maximum_media_duration   
        self.media_duration = new_duration
        # print("New Duration:", self.media_duration)
