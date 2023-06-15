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
        self.setScene(scene)


class GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)


class TimelineWidget(QWidget):

    def __init__(self):
        super().__init__()
        scene_width = 800
        scene_height = 175
        self.setGeometry(500, 500, scene_width + 20, scene_height + 20)

        self.scene = GraphicsScene(scene_width, scene_height)
        self.view = GraphicsView(self.scene)

        self.ruler = Ruler()
        self.handle = RulerHandle()
        self.video_item = MediaItem()

        self.scene.addItem(self.ruler)
        self.scene.addItem(self.video_item)
        self.scene.addItem(self.handle)

        placement_offset_x = 10
        self.ruler.setPos(placement_offset_x, 20)
        self.handle.setPos(placement_offset_x, 0)
        self.video_item.setPos(placement_offset_x, 55)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)
