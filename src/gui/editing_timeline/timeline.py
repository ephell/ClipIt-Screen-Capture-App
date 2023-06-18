"""Importable widget containing all timeline related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .ruler_handle import RulerHandle
from .media_item import MediaItem
from .ruler import Ruler


class GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.media_item_x = 50
        self.media_item_y = 55
        self.ruler_x = 50
        self.ruler_y = 20
        self.ruler_handle_x = 50
        self.ruler_handle_y = 0


class GraphicsView(QGraphicsView):

    resize_signal = Signal(int, int)

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
        old_width = self.scene.width()
        new_width = event.size().width()
        new_height = event.size().height()
        self.scene.setSceneRect(0, 0, new_width, new_height)
        self.resize_signal.emit(new_width, old_width)


class TimelineWidget(QWidget):

    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player

        self.scene = GraphicsScene(800, 200)
        self.view = GraphicsView(self.scene)

        self.ruler_handle = RulerHandle(self.scene, self.media_player.duration())
        self.media_item = MediaItem(self.scene, self.media_player.duration())
        self.ruler = Ruler(self.scene, self.media_player.duration())

        self.view.resize_signal.connect(self.ruler.on_view_resize)
        self.view.resize_signal.connect(self.media_item.on_view_resize)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
