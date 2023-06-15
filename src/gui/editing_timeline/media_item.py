from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaItem(QGraphicsRectItem):
    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.setPos(30, 55)
        self.setRect(QRectF(0, 0, self.scene.width() - self.pos().x() * 2, 100))
        self.setPen(QPen(Qt.blue, 1))
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)
        self.original_width = self.rect().width()
        self.minimum_width = 1
        self.media_duration = media_duration
        self.maximum_media_duration = media_duration
        self.right_handle = _RightHandle(self)
        self.left_handle = _LeftHandle(self)

    """Override"""
    def setRect(self, *args):
        if len(args) == 4:
            super().setRect(*args)
        elif len(args) == 1 and isinstance(args[0], QRectF):
            super().setRect(args[0])
        else:
            raise ValueError("Invalid arguments for setRect")
        
        # print(
        #     f"Width: {self.rect().width()}, Height: {self.rect().height()} ||| "
        #     f"X: {self.rect().x()}, Y: {self.rect().y()}"
        # )

    def adjust_duration(self):
        duration_ratio = self.rect().width() / self.original_width
        new_duration = duration_ratio * self.maximum_media_duration   
        self.media_duration = new_duration
        # print(f"New duration: {self.media_duration}")


class _RightHandle(QGraphicsRectItem):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setRect(0, 0, 15, self.parent.rect().height())
        self.setPen(QPen(Qt.red, 1))
        self.setPos(
            parent.pos().x() + parent.rect().width(),
            parent.pos().y()
        )
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

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
                self.parent.adjust_duration()
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
        self.setPos(
            parent.pos().x() - self.rect().width(),
            parent.pos().y()
        )
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

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
                self.parent.adjust_duration()
                return QPointF(value.x(), self.parent.pos().y())
            return QPointF(self.pos().x(), self.parent.pos().y())
        return super().itemChange(change, value)
