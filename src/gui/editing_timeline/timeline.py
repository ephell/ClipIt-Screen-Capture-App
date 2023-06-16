"""Importable widget containing all timeline related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .ruler_handle import RulerHandle
from .media_item import MediaItem
from .ruler import Ruler


class GraphicsView(QGraphicsView):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumSize(self.scene.width(), self.scene.height())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


class GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        # Try keeping x offsets the same
        self.media_item_x = 30
        self.media_item_y = 55
        self.ruler_x = 30
        self.ruler_y = 20
        self.ruler_handle_x = 30
        self.ruler_handle_y = 0


class TimelineWidget(QWidget):

    def __init__(self):
        super().__init__()
        scene_width = 800
        scene_height = 200
        self.setGeometry(500, 500, scene_width + 20, scene_height + 20)

        self.scene = GraphicsScene(scene_width, scene_height)
        self.view = GraphicsView(self.scene)

        self.ruler_handle = RulerHandle(self.scene, 10000)
        self.media_item = MediaItem(self.scene, 10000)
        self.ruler = Ruler(self.scene, 10000)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
