"""Importable widget containing all timeline related components."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QSizePolicy, QGraphicsScene, QGraphicsView, QWidget, QVBoxLayout
)

from .media_item.media_item import MediaItem
from .ruler.ruler import Ruler


class Timeline(QWidget):

    def __init__(self, media_duration, parent=None):
        super().__init__(parent)
        self.media_duration = media_duration
        self.scene = _GraphicsScene(740, 160)
        self.view = _GraphicsView(self.scene)
        self.ruler = Ruler(self.scene, self.view, self.media_duration)
        self.media_item = MediaItem(self.scene, self.media_duration)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.view.resize_ruler.connect(self.ruler.on_view_resize)
        self.view.resize_media_item.connect(self.media_item.on_view_resize)
        self.scene.ruler_handle_time_changed.connect(
            self.media_item.on_ruler_handle_time_changed
        )
        self.scene.media_item_left_handle_moved.connect(
            self.ruler.ruler_handle.on_media_item_left_handle_moved
        )
        self.scene.media_item_right_handle_moved.connect(
            self.ruler.ruler_handle.on_media_item_right_handle_moved
        )
        self.scene.media_item_start_time_changed.connect(
            self.ruler.ruler_handle.on_media_item_start_time_changed
        )
        self.scene.media_item_end_time_changed.connect(
            self.ruler.ruler_handle.on_media_item_end_time_changed
        )


class _GraphicsScene(QGraphicsScene):

    ruler_handle_time_changed = Signal(int)
    media_item_left_handle_moved = Signal(int)
    media_item_right_handle_moved = Signal(int)
    media_item_start_time_changed = Signal(int)
    media_item_end_time_changed = Signal(int)

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.media_item_x = 50
        self.media_item_y = 50
        self.ruler_x = 50
        self.ruler_y = 0


class _GraphicsView(QGraphicsView):

    resize_ruler = Signal()
    resize_media_item = Signal()

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(self.scene.width())
        self.setMaximumHeight(self.scene.height())

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.resize_ruler.emit()
        self.resize_media_item.emit()

    def resize_scene(self, new_width):
        """
        Called after calculating the new scene size in the ruler. Make
        sure the first connected slot is the ruler's 'on_view_resize'.
        """
        self.scene.setSceneRect(0, 0, new_width, self.contentsRect().height())
