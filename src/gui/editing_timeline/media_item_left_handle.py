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
        self.handle_width = 20
        self.handle_height = self.parent.initial_height
        self.setRect(0, 0, self.handle_width, self.handle_height)
        self.left_pad_x = self.parent.scene.media_item_x
        self.right_pad_x = self.parent.scene.media_item_x
        self.initial_x = self.left_pad_x - self.handle_width
        self.initial_y = self.parent.scenePos().y()
        self.setPos(self.initial_x, self.initial_y)
        self.media_duration = self.parent.media_duration
        self.delta_needed_to_move = 10
        self.move_by_ms = 50

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red, 1))
        painter.drawRect(self.boundingRect())

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.previous_scene_pos = event.scenePos()
            self.started_dragging = True
            self.x_at_drag_start = self.scenePos().x()
            self.previous_width_diff = 0
            event.accept()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.started_dragging = False
            event.accept()

    """Override"""
    def mouseMoveEvent(self, event):
        if self.started_dragging:
            delta_x = event.scenePos().x() - self.scenePos().x()
            new_x = self.__get_new_x(delta_x)

            current_width_diff = self.x_at_drag_start - new_x
            if self.previous_width_diff != current_width_diff:
                delta_width = self.previous_width_diff - current_width_diff
                self.previous_width_diff = current_width_diff

                available_width = self.parent.rect().width()
                new_width = available_width
                if delta_x >= self.delta_needed_to_move and available_width > 0:
                    new_width = available_width - abs(delta_width)
                elif delta_x <= -self.delta_needed_to_move:
                    new_width = available_width + abs(delta_width)

                min_duration = self.__convert_time_to_pixels(self.move_by_ms)
                current_x_time = self.__convert_scene_x_to_time(new_x)
                current_duration = self.parent.end_time - current_x_time
                current_duration = self.__convert_time_to_pixels(current_duration)
                if (
                    new_width != available_width 
                    and current_duration >= min_duration
                ):
                    self.parent.setPos(
                        new_x + self.rect().width(), 
                        self.parent.scenePos().y()
                    )
                    self.parent.setRect(
                        self.parent.rect().x(), 
                        self.parent.rect().y(), 
                        new_width, 
                        self.parent.rect().height()
                    )
                    self.parent.update_start_time(
                        self.__convert_scene_x_to_time(new_x)
                    )
                    self.setPos(new_x, self.scenePos().y())

    def __get_new_x(self, delta_x):
        if delta_x >= self.delta_needed_to_move:
            new_x = self.__get_new_x_when_delta_increasing(self.move_by_ms)
        elif delta_x <= -self.delta_needed_to_move:
            new_x = self.__get_new_x_when_delta_decreasing(self.move_by_ms)
        elif -self.delta_needed_to_move < delta_x < self.delta_needed_to_move:
            new_x = self.scenePos().x()
        return new_x

    def __get_new_x_when_delta_increasing(self, move_by_ms):
        new_x = self.scenePos().x() + self.__convert_time_to_pixels(move_by_ms)
        if new_x >= self.__get_max_possible_x():
            new_x = self.__get_max_possible_x()
        return new_x

    def __get_new_x_when_delta_decreasing(self, move_by_ms):
        new_x = self.scenePos().x() - self.__convert_time_to_pixels(move_by_ms)
        if new_x <= self.__get_min_possible_x():
            new_x = self.__get_min_possible_x()
        # Removing remainder of time if it exists so that the handle
        # moves in equal increments of time.
        if self.scenePos().x() == self.__get_max_possible_x():
            current_time = self.__convert_pixels_to_time(
                self.__get_max_possible_width()
            )
            time_remainder = current_time % move_by_ms
            if time_remainder != 0:
                closest_whole_time = current_time - time_remainder
                new_x = self.__convert_time_to_scene_x(closest_whole_time)
        return new_x
        
    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()
    
    def __get_min_possible_x(self):
        return self.left_pad_x - self.handle_width

    def __get_max_possible_width(self):
        return self.scene().width() - self.left_pad_x - self.right_pad_x

    def __convert_time_to_pixels(self, time):
        return time / self.__get_one_pixel_time_value()
    
    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())
    
    def __convert_time_to_scene_x(self, time):
        return self.__convert_time_to_pixels(time) + self.__get_min_possible_x()
    
    def __convert_scene_x_to_time(self, scene_x):
        return self.__convert_pixels_to_time(scene_x - self.__get_min_possible_x())
