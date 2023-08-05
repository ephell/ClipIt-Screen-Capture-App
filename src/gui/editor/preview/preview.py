"""Importable widget containing all video preview related components."""

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QSizePolicy
)

from ._media_player import MediaPlayer
from ._media_player_controls.media_player_controls import MediaPlayerControls


class Preview(QWidget):

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.scene = _GraphicsScene(740, 400, self)
        self.view = _GraphicsView(self.scene, self)
        self.media_player = MediaPlayer(self.scene, file_path, self)
        self.media_player_controls = MediaPlayerControls(self.media_player, self)
        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.media_player_controls)
        self.setLayout(self.layoutas)
        self.media_player.pause()
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.view.view_resized.connect(
            self.__stretch_and_center_video_output_and_cropper
        )
        self.scene.video_output_native_size_changed_signal.connect(
            self.media_player_controls.crop_button.set_max_cropper_rect
        )
        self.scene.video_output_native_size_changed_signal.connect(
            self.__stretch_and_center_video_output_and_cropper
        )
        self.scene.cropper_resized_signal.connect(
            self.media_player.video_output.on_cropper_resized_signal
        )
        
    @Slot()
    def __stretch_and_center_video_output_and_cropper(self):
        self.media_player.video_output.center_in_scene()
        if self.media_player_controls.crop_button.cropper is not None:
            self.media_player_controls.crop_button.cropper.setPos(
                self.media_player.video_output.pos()
            )
        self.view.fitInView(self.media_player.video_output, Qt.KeepAspectRatio)


class _GraphicsScene(QGraphicsScene):

    cropper_resized_signal = Signal(int, int, int, int)
    video_output_native_size_changed_signal = Signal(int, int)

    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, width, height)
        self.initial_width = width
        self.initial_height = height
        self.setBackgroundBrush(QColor(70, 70, 70))


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

    """Override"""
    def fitInView(self, item, aspectRatioMode=Qt.IgnoreAspectRatio):
        if isinstance(item, QGraphicsVideoItem):
            # Leaves empty space between the video output and the views borders.
            top_offset = 20
            bottom_offset = 20
            left_offset = 10
            right_offset = 10
            item_rect = item.boundingRect()
            adjusted_rect = item_rect.adjusted(
                -left_offset, -bottom_offset, right_offset, top_offset
            )
            super().fitInView(adjusted_rect, aspectRatioMode)
        else:
            super().fitInView(item, aspectRatioMode)
