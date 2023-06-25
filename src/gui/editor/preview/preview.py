"""Importable widget containing all video preview related components."""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from ._media_player import MediaPlayer
from ._media_slider import MediaSlider
from ._media_buttons import MediaButtons


class _GraphicsScene(QGraphicsScene):

    def __init__(self, width, height):
        super().__init__()
        self.setSceneRect(0, 0, width, height)


class _GraphicsView(QGraphicsView):

    view_resized = Signal()

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setScene(scene)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view_resized.emit()


class Preview(QWidget):

    def __init__(self):
        super().__init__()
        
        self.scene = _GraphicsScene(600, 400)
        self.view = _GraphicsView(self.scene)

        self.media_player = MediaPlayer(self.scene)
        self.media_slider = MediaSlider(self.media_player)
        self.media_buttons = MediaButtons(self.media_player)

        # Connecting to 'nativeSizeChanged' stretches video output 
        # properly once it's loaded for the first time.
        self.media_player.video_output.nativeSizeChanged.connect(
            self.__stretch_video_output
        )
        self.view.view_resized.connect(self.__stretch_video_output)
        self.media_player.play()

        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.media_buttons)
        self.layoutas.addWidget(self.media_slider)
        self.setLayout(self.layoutas)

    def get_media_player(self):
        return self.media_player
    
    @Slot()
    def __stretch_video_output(self):
        self.view.fitInView(self.media_player.video_output, Qt.IgnoreAspectRatio)
