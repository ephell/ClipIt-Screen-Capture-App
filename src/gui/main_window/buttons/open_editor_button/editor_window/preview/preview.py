"""Importable widget containing all video preview related components."""

from PySide6.QtCore import Qt, Slot, Signal, QSize
from PySide6.QtGui import QPainter, QColor, QResizeEvent
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QSizePolicy
)

from ._media_player.media_player import MediaPlayer
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
        self.setLayout(self.layoutas)
        self.__connect_signals_and_slots()
        # Required to trigger the initial paint event.
        self.media_player.pause()

    def __connect_signals_and_slots(self):
        # Make sure this signal is always connected before stretching
        # and centering the video output and cropper. Otherwise the
        # cropper will be offcenter when it's first shown.
        self.scene.video_output_native_size_changed_signal.connect(
            self.__set_max_cropper_rect
        )
        self.scene.video_output_native_size_changed_signal.connect(
            self.view.set_max_scene_dimensions
        )
        self.scene.video_output_native_size_changed_signal.connect(
            self.__stretch_and_center_video_output_and_cropper
        )
        self.scene.video_output_native_size_changed_signal.connect(
            self.media_player_controls.crop_button.resolution_label_container.resolution_label.on_video_output_native_size_changed_signal
        )
        self.scene.cropper_resized_signal.connect(
            self.media_player.video_output.on_cropper_resized_signal
        )
        self.scene.cropper_resized_signal.connect(
            self.media_player_controls.crop_button.resolution_label_container.resolution_label.on_cropper_resized_signal
        )
        self.view.view_resized.connect(
            self.__stretch_and_center_video_output_and_cropper
        )
        
    @Slot()
    def __stretch_and_center_video_output_and_cropper(self):
        self.media_player.video_output.center_in_scene()
        if self.media_player_controls.crop_button.cropper is not None:
            self.media_player_controls.crop_button.cropper.setPos(
                self.media_player.video_output.pos()
            )
        self.view.fitInView(self.media_player.video_output, Qt.KeepAspectRatio)

    @Slot()
    def __set_max_cropper_rect(self, width, height):
        self.media_player_controls.crop_button.set_max_cropper_rect(width, height)


class _GraphicsScene(QGraphicsScene):

    cropper_resized_signal = Signal(int, int, int, int)
    video_output_native_size_changed_signal = Signal(int, int)

    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.setSceneRect(0, 0, width, height)
        self.initial_width = width
        self.initial_height = height
        self.setBackgroundBrush(QColor(65, 65, 65))


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
        self.max_scene_w = None
        self.max_scene_h = None
        self.__is_first_set_max_scene_dimensions = True

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.max_scene_w is None or self.max_scene_h is None:
            self.scene.setSceneRect(0, 0, event.size().width(), event.size().height())
        else:
            self.scene.setSceneRect(0, 0, self.max_scene_w, self.max_scene_h)
        self.view_resized.emit()

    """Override"""
    def fitInView(self, item, aspectRatioMode=Qt.IgnoreAspectRatio):
        if isinstance(item, QGraphicsVideoItem):
            # Prevents the video output being fit perfectly into the view by
            # adding some offsets. This is done so that the video cropper's
            # handles are always visible.
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

    def set_max_scene_dimensions(self, width, height):
        """
        Setting fixed scene dimensions allows for a more precise centering
        of the video output and cropper. Also completely prevents the 
        scene/view from being scrollable.
        """
        self.max_scene_w = width
        self.max_scene_h = height

        # This is required to correctly center the video output on the first
        # resize event (when the window is first shown). Videos with resolutions
        # under 350x350 are not centered correctly and may even appear completely 
        # off view if this is omitted.
        if self.__is_first_set_max_scene_dimensions:
            self.__is_first_set_max_scene_dimensions = False
            self.resizeEvent(QResizeEvent(QSize(width, height), self.size()))
