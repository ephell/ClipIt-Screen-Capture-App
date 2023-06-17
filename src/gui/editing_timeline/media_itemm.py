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
        self.setPos(self.scene.media_item_x, self.scene.media_item_y)
        self.__initial_width = self.scene.width() - self.pos().x() * 2
        self.__initial_height = 100
        self.setRect(0, 0, self.__initial_width, self.__initial_height)
        self.left_handle = LeftHandle(self)
        self.right_handle = RightHandle(self)
        self.media_duration = media_duration

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.blue, 1))
        painter.drawRect(self.boundingRect())

    @Slot()
    def on_view_resize(self, old_scene_w, new_scene_w):
        pass
    
        
class RightHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.__initial_width = 20
        self.__initial_height = self.parent.rect().height()
        self.setRect(0, 0, self.__initial_width, self.__initial_height)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.set_position(
            self.parent.pos().x() + self.parent.rect().width() - self.rect().width(), 
            self.parent.pos().y()
        )

    def set_position(self, new_x, new_y):
        self.setPos(new_x, new_y)

    def recalculate_position(self):
        new_x = self.parent.pos().x() + self.parent.rect().width() - self.rect().width()
        new_y = self.parent.pos().y()
        self.set_position(new_x, new_y)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red, 1))
        painter.drawRect(self.boundingRect())

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.scenePos()
            self.previous_scene_pos = event.scenePos()
            event.accept()

    """Override"""
    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None:
            delta = event.scenePos().x() - self.previous_scene_pos.x()
            new_parent_rect_x = self.parent.rect().x()
            new_parent_rect_y = self.parent.rect().y()
            new_parent_rect_width = self.parent.rect().width() + delta
            new_parent_rect_height = self.parent.rect().height()
            new_handle_x = self.pos().x() + delta
            new_handle_y = self.pos().y()
            # Prevents media item from being dragged off further than
            # the width of the scene
            max_width = (self.parent.scene.width() - self.parent.pos().x() * 2)
            avail_width = max_width - new_parent_rect_width
            # Prevents right handle from being dragged over left handle
            min_width = self.__initial_width * 2
            if (
                new_parent_rect_width > 0
                and new_parent_rect_width > min_width
                and avail_width > 0
            ):
                self.parent.setRect(
                    new_parent_rect_x,
                    new_parent_rect_y,
                    new_parent_rect_width,
                    new_parent_rect_height
                )
                self.set_position(new_handle_x, new_handle_y)
            self.previous_scene_pos = event.scenePos()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
            event.accept()


class LeftHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.__initial_width = 20
        self.__initial_height = self.parent.rect().height()
        self.setRect(0, 0, self.__initial_width, self.__initial_height)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.set_position(self.parent.pos().x(), self.parent.pos().y())
        self.minimum_x = self.parent.pos().x()

    def set_position(self, new_x, new_y):
        self.setPos(new_x, new_y)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red, 1))
        painter.drawRect(self.boundingRect())

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.scenePos()
            self.previous_scene_pos = event.scenePos()
            event.accept()

    """Override"""
    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None:
            delta = event.scenePos().x() - self.previous_scene_pos.x()
            new_parent_rect_x = self.parent.rect().x() + delta
            new_parent_rect_y = self.parent.rect().y()
            new_parent_rect_width = self.parent.rect().width() - delta
            new_parent_rect_height = self.parent.rect().height()
            new_handle_x = self.pos().x() + delta
            new_handle_y = self.pos().y()
            # Prevents left handle from being dragged over right handle
            min_width = self.__initial_width * 2
            if (
                new_parent_rect_width > 0
                and new_handle_x > self.minimum_x
                and new_parent_rect_width > min_width
            ):
                self.parent.setRect(
                    new_parent_rect_x,
                    new_parent_rect_y,
                    new_parent_rect_width,
                    new_parent_rect_height
                )
                self.set_position(new_handle_x, new_handle_y)
            self.previous_scene_pos = event.scenePos()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
            event.accept()
