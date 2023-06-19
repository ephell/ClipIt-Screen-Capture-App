from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class RightHandle(QGraphicsRectItem):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.scene.addItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.initial_width = 20
        self.initial_height = self.parent.initial_height
        self.setRect(0, 0, self.initial_width, self.initial_height)
        self.initial_x = self.parent.scenePos().x() + self.parent.rect().width()
        self.initial_y = self.parent.scenePos().y()
        self.setPos(self.initial_x, self.initial_y)

    
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
            new_parent_pos_x = int(self.parent.scenePos().x())
            new_parent_pox_y = int(self.parent.scenePos().y())
            new_parent_rect_x = int(self.parent.rect().x())
            new_parent_rect_y = int(self.parent.rect().y())
            new_parent_rect_width = int(self.parent.rect().width() + delta)
            new_parent_rect_height = int(self.parent.rect().height())
            max_parent_rect_width = self.parent.calculate_max_possible_width()
            available_width = max_parent_rect_width - new_parent_rect_width
            max_parent_top_right_x = max_parent_rect_width + self.parent.initial_x - delta
            parent_top_right_x = self.parent.scenePos().x() + self.parent.rect().width()
            if (
                new_parent_rect_width > 0
                and available_width >= 0 # Prevent handle overlap
                and parent_top_right_x <= max_parent_top_right_x # Prevent handle out of bounds
            ):
                self.parent.setPos(new_parent_pos_x, new_parent_pox_y)
                self.parent.setRect(
                    new_parent_rect_x,
                    new_parent_rect_y,
                    new_parent_rect_width,
                    new_parent_rect_height
                )
                self.calculate_and_update_end_time()
                self.update_position()
            self.previous_scene_pos = event.scenePos()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = None
            event.accept()

    def update_position(self):
        self.setPos(
            self.parent.scenePos().x() + self.parent.rect().width(), 
            self.parent.scenePos().y()
        )

    def calculate_and_update_end_time(self):
        parent_top_right_x = self.parent.scenePos().x() + self.parent.rect().width()
        end_time = self.parent.calculate_time_from_x_pos(parent_top_right_x)
        self.parent.update_end_time(end_time)
