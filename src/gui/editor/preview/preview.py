"""Importable widget containing all video preview related components."""

from PySide6.QtCore import Qt, Slot, QSize, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QSizePolicy
)

from ._media_player import MediaPlayer
from ._media_buttons import MediaButtons


class Preview(QWidget):

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.scene = _GraphicsScene(740, 400, self)
        self.view = _GraphicsView(self.scene, self)
        self.media_player = MediaPlayer(self.scene, file_path, self)
        self.media_buttons = MediaButtons(self.media_player, self)
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


class _GraphicsScene(QGraphicsScene):

    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, width, height)
        self.initial_width = width
        self.initial_height = height


class _GraphicsView(QGraphicsView):

    view_resized = Signal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)
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
