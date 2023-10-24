from PySide6.QtCore import Qt, Slot, QRectF
from PySide6.QtGui import QPen, QPainterPath, QBrush, QColor
from PySide6.QtWidgets import QGraphicsItem, QGraphicsWidget

from ._ruler_handle_time_edit import RulerHandleTimeEdit


class RulerHandle(QGraphicsItem):
    
    def __init__(self, ruler, media_duration):
        super().__init__()
        self.ruler = ruler
        self.scene = self.ruler.scene
        self.scene.addItem(self)
        self.setFlag(QGraphicsWidget.ItemIsMovable, True)
        self.setFlag(QGraphicsWidget.ItemIsFocusable, True)
        self.media_duration = media_duration
        self.width = 11
        self.height = 69 + self.scene.media_item_y
        self.left_pad_x = self.scene.ruler_x
        self.right_pad_x = self.scene.ruler_x
        self.top_pad_y = 0
        self.initial_x = self.__get_min_possible_x()
        self.initial_y = self.top_pad_y
        self.setPos(self.initial_x, self.initial_y)
        self.head_width = self.width
        self.head_height = self.height / 12
        self.needle_width = 1
        self.needle_height = self.height - self.head_height
        self.needle_x = (self.width - self.needle_width) / 2
        self.needle_y = self.head_height
        self.no_focus_color = QColor(255, 255, 255)
        self.in_focus_color = QColor(31, 143, 221)
        self.time_edit = RulerHandleTimeEdit(self.scene, self.media_duration)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.time_edit.time_changed_via_ui_signal.connect(
            self.__on_ruler_handle_time_edit_time_changed_via_ui
        )
        self.time_edit.time_changed_via_code_signal.connect(
            self.__on_ruler_handle_time_edit_time_changed_via_code
        )

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    """Override"""
    def paint(self, painter, option, widget):
        if self.hasFocus():
            painter.setPen(QPen(self.in_focus_color))
            painter.setBrush(QBrush(self.in_focus_color))
        elif not self.hasFocus():
            painter.setPen(QPen(self.no_focus_color))
            painter.setBrush(QBrush(self.no_focus_color))
        painter.drawRect(QRectF(0, 0, self.head_width, self.head_height))
        painter.drawRect(QRectF(
            self.needle_x, self.needle_y, 
            self.needle_width, self.needle_height
        ))

    """Override"""
    def shape(self):
        path = QPainterPath()
        path.addRect(0, 0, self.head_width, self.head_height)
        return path

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    """Override"""
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.__move_by_mouse(event.scenePos())

    """Override"""
    def keyPressEvent(self, event):
        if self.hasFocus():
            if event.key() == Qt.Key_Left:
                self.__move_by_key(-1)
            elif event.key() == Qt.Key_Right:
                self.__move_by_key(1)

    @Slot()
    def on_media_player_position_changed(self, time):
        self.setPos(
            self.__get_x_pos_from_time(time), 
            self.scenePos().y()
        )   
        self.time_edit.update_time(time)

    @Slot()
    def on_media_item_left_handle_moved(self, time):
        if time > self.time_edit.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_edit.update_time(time)
            self.scene.ruler_handle_time_changed.emit(time)

    @Slot()
    def on_media_item_right_handle_moved(self, time):
        if time < self.time_edit.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_edit.update_time(time)
            self.scene.ruler_handle_time_changed.emit(time)

    @Slot()
    def on_media_item_start_time_changed(self, time):
        if time > self.time_edit.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_edit.update_time(time)
            self.scene.ruler_handle_time_changed.emit(time)

    @Slot()
    def on_media_item_end_time_changed(self, time):
        if time < self.time_edit.get_time():
            self.setPos(
                self.__get_x_pos_from_time(time),
                self.scenePos().y()
            )
            self.time_edit.update_time(time)
            self.scene.ruler_handle_time_changed.emit(time)

    @Slot()
    def __on_ruler_handle_time_edit_time_changed_via_ui(self, time):
        self.setPos(
            self.__get_x_pos_from_time(time),
            self.scenePos().y()
        )
        self.update()
        self.scene.ruler_handle_time_changed.emit(self.__get_current_time())

    @Slot()
    def __on_ruler_handle_time_edit_time_changed_via_code(self, time):
        self.setPos(
            self.__get_x_pos_from_time(time),
            self.scenePos().y()
        )
        self.update()

    def on_view_resize(self):
        """Not a slot. Called in 'Ruler' object."""
        self.setPos(
            self.__get_x_pos_from_time(self.time_edit.get_time()), 
            self.scenePos().y()
        )

    def on_ruler_left_mouse_clicked(self, click_pos):
        """Not a slot. Called in 'Ruler' object."""
        self.setFocus()
        self.__move_by_mouse(click_pos)

    def __move_by_mouse(self, position):
        new_x = position.x() - self.width / 2
        if new_x <= self.__get_min_possible_x():
            new_x = self.__get_min_possible_x()
        elif new_x >= self.__get_max_possible_x():
            new_x = self.__get_max_possible_x()
        self.setPos(new_x, self.scenePos().y())
        self.time_edit.update_time(self.__get_current_time())
        self.scene.ruler_handle_time_changed.emit(self.__get_current_time())

    def __move_by_key(self, move_by_amount_px):
        current_pos = self.scenePos()
        new_x = current_pos.x() + move_by_amount_px
        if new_x <= self.__get_min_possible_x():
            new_x = self.__get_min_possible_x()
        elif new_x >= self.__get_max_possible_x():
            new_x = self.__get_max_possible_x()
        self.setPos(new_x, current_pos.y())
        self.time_edit.update_time(self.__get_current_time())
        self.scene.ruler_handle_time_changed.emit(self.__get_current_time())

    def __get_max_possible_width(self):
        return self.scene.width() - self.left_pad_x - self.right_pad_x

    def __get_min_possible_x(self):
        return self.left_pad_x - self.width / 2

    def __get_max_possible_x(self):
        return self.__get_min_possible_x() + self.__get_max_possible_width()
    
    def __get_one_pixel_time_value(self):
        return self.media_duration / self.__get_max_possible_width()
    
    def __get_current_time(self):
        current_position = self.scenePos().x() - self.__get_min_possible_x()
        return self.__convert_pixels_to_time(current_position)
    
    def __get_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def __convert_pixels_to_time(self, pixels):
        return round(pixels * self.__get_one_pixel_time_value())
