from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPixmap, QBrush
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem


class RightHandle(QGraphicsRectItem):

    __FILL_IMAGE_PATH = "src/gui/main_window/buttons/open_editor_button/editor_window/timeline/media_item/media_item_handle.jpg"

    def __init__(self, media_item):
        super().__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.parent = media_item
        self.parent.scene.addItem(self)
        self.handle_width = 16
        self.handle_height = self.parent.initial_height
        self.setRect(0, 0, self.handle_width, self.handle_height)
        self.left_pad_x = self.parent.scene.media_item_x
        self.right_pad_x = self.parent.scene.media_item_x
        self.initial_x = self.left_pad_x
        self.initial_y = self.parent.scenePos().y()
        self.setPos(self.initial_x, self.initial_y)
        self.media_duration = self.parent.media_duration
        self.__fill_image =  QPixmap(self.__FILL_IMAGE_PATH)
        self.__scaled_fill_image = self.__fill_image.scaled(
            self.boundingRect().size().toSize(), 
            Qt.KeepAspectRatio
        )

    """Override"""
    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(self.__scaled_fill_image))
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
                new_parent_rect_width += abs(delta)
                new_handle_x += abs(delta)
            elif self.__is_within_decrease_bounds(event.scenePos()):
                new_parent_rect_width -= abs(delta)
                new_handle_x -= abs(delta)

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
                self.parent.update_end_time(self.__get_current_time())
                self.scene().media_item_right_handle_moved.emit(self.__get_current_time())

            self.previous_scene_pos = event.scenePos()

    """Override"""
    def keyPressEvent(self, event):
        if self.hasFocus():
            move_by_amount_px = self.__get_one_ms_pixel_value()
            if event.key() == Qt.Key_Left:
                self.__move_by_key(-move_by_amount_px)
            elif event.key() == Qt.Key_Right:
                self.__move_by_key(move_by_amount_px)
    
    def __move_by_key(self, move_by_amount_px):
        new_parent_rect_x = self.parent.rect().x()
        new_parent_rect_y = self.parent.rect().y()
        new_parent_rect_width = self.parent.rect().width()
        new_parent_rect_height = self.parent.rect().height()
        new_handle_x = self.pos().x()
        new_handle_y = self.pos().y()

        if move_by_amount_px < 0:
            new_parent_rect_width -= abs(move_by_amount_px)
            new_handle_x -= abs(move_by_amount_px)
        elif move_by_amount_px > 0:
            new_parent_rect_width += abs(move_by_amount_px)
            new_handle_x += abs(move_by_amount_px)

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
            self.parent.update_end_time(self.__get_current_time())
            self.scene().media_item_right_handle_moved.emit(self.__get_current_time())

    def __is_within_increase_bounds(self, scene_pos):
        x = self.scenePos().x() + self.handle_width
        y = self.scenePos().y()
        width = 10000
        height = self.rect().height()
        return QRectF(x, y, width, height).contains(scene_pos)

    def __is_within_decrease_bounds(self, scene_pos):
        x = -10000
        y = self.scenePos().y()
        width = self.scenePos().x() - x
        height = self.rect().height()
        return QRectF(x, y, width, height).contains(scene_pos)

    def __get_max_possible_width(self):
        return self.scene().width() - self.left_pad_x - self.right_pad_x

    def __get_min_possible_x(self):
        return self.left_pad_x

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()  

    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()
    
    def __get_one_ms_pixel_value(self):
        return self.__get_max_possible_width() / self.media_duration

    def __get_current_time(self):
        current_position = self.scenePos().x() - self.__get_min_possible_x()
        return self.__convert_pixels_to_time(current_position)

    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())
