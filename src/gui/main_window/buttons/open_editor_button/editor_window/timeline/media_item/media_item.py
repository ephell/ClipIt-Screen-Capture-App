from PySide6.QtCore import Qt, Slot, QRectF
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QGraphicsRectItem

from ._media_item_left_handle import LeftHandle
from ._media_item_right_handle import RightHandle
from ._media_item_time_edits.media_item_time_edits import TimeEdits
from ._thumbnail_creator import ThumbnailCreator


class MediaItem(QGraphicsRectItem):

    def __init__(self, scene, media_player):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.media_player = media_player
        self.media_duration = self.media_player.duration()
        self.start_time = 0
        self.end_time = self.media_duration
        self.left_pad_x = self.scene.media_item_x
        self.right_pad_x = self.scene.media_item_x
        self.top_pad_y = self.scene.media_item_y
        self.initial_x = self.left_pad_x
        self.initial_y = self.top_pad_y
        self.setPos(self.initial_x, self.initial_y)
        self.initial_width = self.__get_width_from_time_interval(
            self.start_time, self.end_time
        )
        self.initial_height = 70
        self.setRect(0, 0, self.initial_width, self.initial_height)
        self.contour_color = QColor(0, 0, 0)
        self.left_handle = LeftHandle(self)
        self.right_handle = RightHandle(self)
        self.time_edits = TimeEdits(scene, self.media_duration)
        self.__thumbnail_creator = ThumbnailCreator(self)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.time_edits.left_handle_time_edit_time_changed_signal.connect(
            self.__on_left_handle_time_edit_time_changed_signal
        )
        self.time_edits.right_handle_time_edit_time_changed_signal.connect(
            self.__on_right_handle_time_edit_time_changed_signal
        )

    """Override"""
    def boundingRect(self):
        return QRectF(0, 0, self.rect().width(), self.rect().height())

    """Override"""
    def paint(self, painter, option, widget):
        if self.__thumbnail_creator is not None:
            painter.setBrush(QBrush(self.__thumbnail_creator.get_thumbnail()))
            painter.drawRect(self.boundingRect())
            painter.setPen(self.contour_color)
            painter.drawRect(self.boundingRect())
        else:
            painter.setBrush(QBrush(Qt.gray))
            painter.drawRect(self.boundingRect())
            painter.setPen(self.contour_color)
            painter.drawRect(self.boundingRect())
    
    def update_start_time(self, time):
        self.start_time = time
        self.time_edits.update_start_time(time)
        self.scene.media_item_start_time_changed.emit(time)

    def update_end_time(self, time):
        self.end_time = time
        self.time_edits.update_end_time(time)
        self.scene.media_item_end_time_changed.emit(time)

    @Slot()
    def on_view_resize(self):
        self.__resize_based_on_time_interval(self.start_time, self.end_time)
        self.__move_to_x_based_on_time(self.start_time)
        self.left_handle.setPos(
            self.scenePos().x() - self.left_handle.handle_width,
            self.scenePos().y()
        )
        self.right_handle.setPos(
            self.scenePos().x() + self.rect().width(),
            self.scenePos().y()
        )
        self.time_edits.on_view_resize()
        self.__thumbnail_creator.on_view_resize()
        self.update()

    @Slot()
    def on_ruler_handle_time_changed(self, time):
        if time < self.start_time:
            self.update_start_time(time)
            self.__resize_based_on_time_interval(time, self.end_time)
            self.__move_to_x_based_on_time(time)
            self.left_handle.setPos(
                self.scenePos().x() - self.left_handle.handle_width,
                self.scenePos().y()
            )
        elif time > self.end_time:
            self.update_end_time(time)
            self.__resize_based_on_time_interval(self.start_time, time)
            self.right_handle.setPos(
                self.scenePos().x() + self.rect().width(),
                self.scenePos().y()
            )

    @Slot()
    def on_editor_closed(self):
        self.__thumbnail_creator.kill_extraction_thread()

    @Slot()
    def __on_left_handle_time_edit_time_changed_signal(self, time):
        self.update_start_time(time)
        self.__resize_based_on_time_interval(time, self.end_time)
        self.__move_to_x_based_on_time(time)
        self.left_handle.setPos(
            self.scenePos().x() - self.left_handle.handle_width,
            self.scenePos().y()
        )
        self.scene.media_item_start_time_changed.emit(time)
    
    @Slot()
    def __on_right_handle_time_edit_time_changed_signal(self, time):
        self.update_end_time(time)
        self.__resize_based_on_time_interval(self.start_time, time)
        self.right_handle.setPos(
            self.scenePos().x() + self.rect().width(),
            self.scenePos().y()
        )
        self.scene.media_item_end_time_changed.emit(time)

    def get_max_possible_width(self):
        return self.scene.width() - self.left_pad_x - self.right_pad_x
    
    def __get_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.get_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def __move_to_x_based_on_time(self, time):
        self.setPos(self.__get_x_pos_from_time(time), self.initial_y)

    def __get_width_from_time_interval(self, start_time, end_time):
        total_time = self.media_duration
        max_possible_width = self.get_max_possible_width()
        return (end_time - start_time) / total_time * max_possible_width

    def __resize_based_on_time_interval(self, start_time, end_time):
        self.setRect(
            0, 
            0,
            self.__get_width_from_time_interval(start_time, end_time), 
            self.initial_height
        )
