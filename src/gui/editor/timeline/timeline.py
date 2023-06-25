"""Importable widget containing all timeline related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from ._ruler import Ruler
from ._media_item import MediaItem


class _GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.media_item_x = 50
        self.media_item_y = 55
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
        self.setMaximumHeight(self.scene.height())
        self.setMinimumWidth(self.scene.width())

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
        self.scene.setSceneRect(0, 0, new_width, self.scene.height())


class Timeline(QWidget):

    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player

        self.scene = _GraphicsScene(800, 200)
        self.view = _GraphicsView(self.scene)

        self.ruler = Ruler(self.scene, self.view, self.media_player.duration())
        self.media_item = MediaItem(self.scene, self.media_player.duration())

        self.view.resize_ruler.connect(self.ruler.on_view_resize)
        self.view.resize_media_item.connect(self.media_item.on_view_resize)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
