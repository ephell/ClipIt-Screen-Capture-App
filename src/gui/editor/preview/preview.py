"""Importable widget containing all video preview related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from ._media_player import MediaPlayer
from ._media_buttons import MediaButtons


class _GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)
        self.initial_width = width
        self.initial_height = height


class _GraphicsView(QGraphicsView):

    view_resized = Signal()

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(
            QPainter.Antialiasing | 
            QPainter.SmoothPixmapTransform | 
            QPainter.TextAntialiasing
        )
        self.setMinimumWidth(self.scene.initial_width)
        self.setMinimumHeight(self.scene.initial_height)

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        self.view_resized.emit()


class Preview(QWidget):

    def __init__(self, file_path):
        super().__init__()
        self.scene = _GraphicsScene(740, 400)
        self.view = _GraphicsView(self.scene)
        self.media_player = MediaPlayer(self.scene, file_path)
        self.media_buttons = MediaButtons(self.media_player)
        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.media_buttons)
        self.setLayout(self.layoutas)

        self.view.view_resized.connect(self.__stretch_video_output)
        self.media_player.pause()

    @Slot()
    def __stretch_video_output(self):
        self.media_player.video_output.setSize(
            QSize(self.scene.width(), self.scene.height())
        )
        self.view.fitInView(self.media_player.video_output, Qt.KeepAspectRatio)
