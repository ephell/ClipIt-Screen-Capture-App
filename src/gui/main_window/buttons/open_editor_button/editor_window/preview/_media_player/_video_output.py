from PySide6.QtCore import Slot, QRectF, QSizeF, Qt
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem


class VideoOutput(QGraphicsVideoItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.scene.addItem(self)
        self.setAspectRatioMode(Qt.KeepAspectRatio)
        self.top_l_x = 0
        self.top_l_y = 0
        self.width = 0
        self.height = 0
        self.nativeSizeChanged.connect(self.__on_native_size_changed)

    """Override"""
    def paint(self, painter, option, widget):
        painter.setClipRect(
            QRectF(self.top_l_x, self.top_l_y, self.width, self.height)
        )
        super().paint(painter, option, widget)

    @Slot()
    def on_cropper_resized_signal(self, top_l_x, top_l_y, width, height):
        """
        Receives the new dimensions of the cropper and triggers a repaint
        of the video output.
        """
        self.top_l_x = top_l_x
        self.top_l_y = top_l_y
        self.width = width
        self.height = height
        self.update()

    @Slot()
    def __on_native_size_changed(self):
        self.width = self.nativeSize().width()
        self.height = self.nativeSize().height()
        self.setSize(QSizeF(self.width, self.height))
        self.scene.video_output_native_size_changed_signal.emit(
            self.width, self.height
        )

    def center_in_scene(self):
        video_width = self.boundingRect().width()
        video_height = self.boundingRect().height()
        scene_width = self.scene.width()
        scene_height = self.scene.height()
        x_pos = (scene_width - video_width) / 2
        y_pos = (scene_height - video_height) / 2
        self.setPos(x_pos, y_pos)

    def get_clip_rect(self):
        """
        Returns the rectangle that represents the currently visible part
        of the video output.
        """
        return (
            int(self.top_l_x), 
            int(self.top_l_y), 
            int(self.width),
            int(self.height)
        )
