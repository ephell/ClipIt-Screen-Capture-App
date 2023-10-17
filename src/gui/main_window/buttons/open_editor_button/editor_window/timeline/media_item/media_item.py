from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPen, QBrush, QPixmap, QImage, QPainter, QColor
from PySide6.QtWidgets import QGraphicsRectItem

from ._media_item_left_handle import LeftHandle
from ._media_item_right_handle import RightHandle
from ._media_item_time_edits.media_item_time_edits import TimeEdits


class MediaItem(QGraphicsRectItem):

    def __init__(self, scene, media_duration):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)
        self.media_duration = media_duration
        self.start_time = 0
        self.end_time = media_duration
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
        self.left_handle = LeftHandle(self)
        self.right_handle = RightHandle(self)
        self.time_edits = TimeEdits(scene, media_duration)
        self.__connect_signals_and_slots()
        # Thumbnail related
        self.__thumbnail_pixmap = None
        self.__initial_thumbnail_pixmap = None
        self.__qimage_list = None

    def __connect_signals_and_slots(self):
        self.time_edits.left_handle_time_edit_time_changed_signal.connect(
            self.__on_left_handle_time_edit_time_changed_signal
        )
        self.time_edits.right_handle_time_edit_time_changed_signal.connect(
            self.__on_right_handle_time_edit_time_changed_signal
        )

    """Override"""
    def paint(self, painter, option, widget):
        if self.__thumbnail_pixmap is None:
            painter.setBrush(QBrush(Qt.gray))
            painter.drawRect(self.boundingRect())
        else:
            painter.setBrush(QBrush(self.__thumbnail_pixmap))
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
        if self.__thumbnail_pixmap is not None:
            self.resize_thumbnail_pixmap()
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

    @Slot()
    def on_finished_collecting_media_item_thumbnail_frames(self, qimage_list):
        self.__thumbnail_pixmap = self.__create_initial_thumbnail_pixmap(qimage_list)
        self.__initial_thumbnail_pixmap = self.__thumbnail_pixmap
        self.__qimage_list = qimage_list
        self.update()

    def __create_initial_thumbnail_pixmap(self, qimage_list):
        width_per_qimage = self.__calculate_width_per_qimage(qimage_list)
        for i, qimage in enumerate(qimage_list):
            qimage_list[i] = qimage.scaled(
                width_per_qimage,
                self.boundingRect().height(),
                mode=Qt.FastTransformation
            )

        thumbnail_width = self.boundingRect().width()
        thumbnail_height = self.boundingRect().height()
        thumbnail_image = QImage(
            thumbnail_width,
            thumbnail_height,
            qimage_list[0].format()
        )
        painter = QPainter(thumbnail_image)
        for i, qimage in enumerate(qimage_list):
            painter.drawImage(i * width_per_qimage, 0, qimage)
        painter.end() 
        thumbnail_image.save("test.png")

        return QPixmap.fromImage(thumbnail_image)

    def __calculate_width_per_qimage(self, qimage_list):
        if self.__initial_thumbnail_pixmap is not None:
            return self.__initial_thumbnail_pixmap.width() / len(qimage_list)
        return self.boundingRect().width() / len(qimage_list)

    def __scale_qimage_list(self, qimage_list):
        width_per_qimage = self.__calculate_width_per_qimage(qimage_list)
        for i, qimage in enumerate(qimage_list):
            qimage_list[i] = qimage.scaled(
                width_per_qimage,
                self.boundingRect().height(),
                mode=Qt.FastTransformation
            )
        return qimage_list

    def __calculate_filler_width(self):
        width_diff = self.boundingRect().width() - self.__initial_thumbnail_pixmap.width()
        return max(0, width_diff / len(self.__qimage_list))

    def __add_fillers_to_qimages(self, qimage_list):
        filler_width = self.__calculate_filler_width()
        filler_color = QColor(Qt.gray)
        new_qimage_list = []
        for qimage in qimage_list:
            new_qimage = QImage(
                qimage.width() + filler_width,
                qimage.height(),
                qimage.format()
            )
            painter = QPainter(new_qimage)
            new_qimage.fill(filler_color)
            painter.drawImage(0, 0, qimage)
            new_qimage_list.append(new_qimage)
            painter.end()
        return new_qimage_list

    def __create_thumbnail_pixmap(self, qimage_list):
        qimage_list = self.__scale_qimage_list(qimage_list)

        filler_width = self.__calculate_filler_width()
        if filler_width > 0:
            qimage_list = self.__add_fillers_to_qimages(qimage_list)

        qimage_width = qimage_list[0].width()
        qimage_height = self.boundingRect().height()
        thumbnail_width = qimage_width * len(qimage_list)
        thumbnail_height = qimage_height
        thumbnail_image = QImage(
            thumbnail_width,
            thumbnail_height,
            qimage_list[0].format()
        )

        painter = QPainter(thumbnail_image)
        for i, qimage in enumerate(qimage_list):
            painter.drawImage(i * qimage_width, 0, qimage)
        painter.end()

        return QPixmap.fromImage(thumbnail_image)

    def resize_thumbnail_pixmap(self):
        self.__thumbnail_pixmap = self.__create_thumbnail_pixmap(self.__qimage_list)

    def __get_max_possible_width(self):
        return self.scene.width() - self.left_pad_x - self.right_pad_x
    
    def __get_x_pos_from_time(self, time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (time / total_time) * max_possible_width + self.initial_x

    def __move_to_x_based_on_time(self, time):
        self.setPos(self.__get_x_pos_from_time(time), self.initial_y)

    def __get_width_from_time_interval(self, start_time, end_time):
        total_time = self.media_duration
        max_possible_width = self.__get_max_possible_width()
        return (end_time - start_time) / total_time * max_possible_width

    def __resize_based_on_time_interval(self, start_time, end_time):
        self.setRect(
            0, 
            0,
            self.__get_width_from_time_interval(start_time, end_time), 
            self.initial_height
        )
