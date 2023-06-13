"""Importable widget containing all timeline related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .handle import RulerHandle
from .media_item import MediaItem
from .ruler import Ruler


class TimelineWidget(QWidget):
    
    def __init__(self):
        super().__init__()        
        scene_x = 800
        scene_y = 175

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.scene.setSceneRect(0, 0, scene_x, scene_y)

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
