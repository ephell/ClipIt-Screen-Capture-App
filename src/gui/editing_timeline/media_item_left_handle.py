from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class LeftHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.initial_width = 20
        self.initial_height = self.parent.initial_height
        self.setRect(0, 0, self.initial_width, self.initial_height)
        self.initial_x = self.parent.x()
        self.initial_y = self.parent.y()
        self.setPos(self.initial_x, self.initial_y)
        self.minimum_x = self.parent.x()

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
            min_width = self.initial_width * 2
            if (
                new_parent_rect_width > 0
                and new_parent_rect_width > min_width # Prevent handle overlap
                and new_handle_x >= self.initial_x # Prevent handle out of bounds
            ):
                self.parent.setRect(
                    new_parent_rect_x,
                    new_parent_rect_y,
                    new_parent_rect_width,
                    new_parent_rect_height
                )
                self.setPos(new_handle_x, new_handle_y)
                self.calculate_and_update_start_time()
            self.previous_scene_pos = event.scenePos()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
            event.accept()

    def update_position(self):
        self.setPos(self.parent.x(), self.parent.y())

    def calculate_and_update_start_time(self):
        handle_top_left_x = self.pos().x()
        start_time = self.parent.calculate_time_from_x_pos(handle_top_left_x)
        self.parent.update_start_time(start_time)
