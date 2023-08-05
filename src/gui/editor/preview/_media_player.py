from PySide6.QtCore import Qt, QUrl, QRectF, QSizeF, Slot
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem


class MediaPlayer(QMediaPlayer):

    def __init__(self, scene, file_path, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.file_path = file_path
        self.source_file = QUrl.fromLocalFile(self.file_path)
        self.setSource(self.source_file)
        self.video_output = _VideoOutput(self.scene)
        self.setVideoOutput(self.video_output)
        self.audio_output = _AudioOutput(self)
        self.setAudioOutput(self.audio_output)
        self.start_time = 0
        self.end_time = self.duration()

    def update_start_time(self, new_start_time):
        self.start_time = new_start_time

    def update_end_time(self, new_end_time):
        self.end_time = new_end_time

    """Override"""
    def stop(self):
        if self.playbackState() == QMediaPlayer.PlayingState:
            self.setPosition(self.start_time)
        else:
            super().stop()
            self.setPosition(self.start_time)

    """Override"""
    def play(self):
        if (
            self.playbackState() == QMediaPlayer.PausedState
            and self.position() >= self.end_time
        ):
            self.setPosition(self.start_time)
            super().play()
        else:
            super().play()


class _VideoOutput(QGraphicsVideoItem):

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
        rectas = QRectF(
            self.top_l_x, 
            self.top_l_y,
            self.width,
            self.height
        )
        painter.setClipRect(rectas)
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


class _AudioOutput(QAudioOutput):

    def __init__(self, parent=None):
        super().__init__(parent)
