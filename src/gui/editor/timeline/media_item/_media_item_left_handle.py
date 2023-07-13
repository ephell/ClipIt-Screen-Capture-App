from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen
from PySide6.QtWidgets import (
    QGraphicsRectItem, QGraphicsItem
)


class LeftHandle(QGraphicsRectItem):

    def __init__(self, media_item):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.parent = media_item
        self.parent.scene.addItem(self)
        self.handle_width = 20
        self.handle_height = self.parent.initial_height
        self.setRect(0, 0, self.handle_width, self.handle_height)
        self.left_pad_x = self.parent.scene.media_item_x
        self.right_pad_x = self.parent.scene.media_item_x
        self.initial_x = self.left_pad_x - self.handle_width
        self.initial_y = self.parent.scenePos().y()
        self.setPos(self.initial_x, self.initial_y)
        self.media_duration = self.parent.media_duration

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red, 1))
        painter.drawRect(self.boundingRect())

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.previous_scene_pos = event.scenePos()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    """Override"""
    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.scenePos().x() - self.previous_scene_pos.x()
            new_parent_rect_x = self.parent.rect().x()
            new_parent_rect_y = self.parent.rect().y()
            new_parent_rect_width = self.parent.rect().width()
            new_parent_rect_height = self.parent.rect().height()
            new_handle_x = self.pos().x()
            new_handle_y = self.pos().y()

            if self.__is_within_increase_bounds(event.scenePos()):
                new_parent_rect_x -= abs(delta)
                new_parent_rect_width += abs(delta)
                new_handle_x -= abs(delta)
            elif self.__is_within_decrease_bounds(event.scenePos()):
                new_parent_rect_x += abs(delta)
                new_parent_rect_width -= abs(delta)
                new_handle_x += abs(delta)

            if (
                new_parent_rect_width > 0
                and new_handle_x >= self.__get_min_possible_x()
                and new_handle_x <= self.__get_max_possible_x()
            ):
                self.parent.setRect(
                    new_parent_rect_x,
                    new_parent_rect_y,
                    new_parent_rect_width,
                    new_parent_rect_height
                )
                self.setPos(new_handle_x, new_handle_y)
                self.parent.update_start_time(self.__get_current_time())
                self.scene().media_item_left_handle_moved.emit(self.__get_current_time())

            self.previous_scene_pos = event.scenePos()

    def __is_within_increase_bounds(self, scene_pos):
        x = -10000
        y = self.scenePos().y()
        width = self.scenePos().x() - x
        height = self.rect().height()
        return QRectF(x, y, width, height).contains(scene_pos)
    
    def __is_within_decrease_bounds(self, scene_pos):
        x = self.scenePos().x() + self.handle_width
        y = self.scenePos().y()
        width = 10000
        height = self.rect().height()
        return QRectF(x, y, width, height).contains(scene_pos)
    
    def __get_max_possible_width(self):
        return self.scene().width() - self.left_pad_x - self.right_pad_x

    def __get_min_possible_x(self):
        return self.left_pad_x - self.handle_width

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()  

    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()
    
    def __get_current_time(self):
        current_position = self.scenePos().x() - self.__get_min_possible_x()
        return self.__convert_pixels_to_time(current_position)

    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())
