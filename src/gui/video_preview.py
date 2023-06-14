import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from editing_timeline.timeline import TimelineWidget


class GraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.IgnoreAspectRatio)


class MediaPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self.video_output = QGraphicsVideoItem()
        self.setVideoOutput(self.video_output)
        # self.audio_output = QAudioOutput()
        # self.setAudioOutput(self.audio_output)
        self.setSource(QUrl("src/gui/editing_timeline/test.mp4"))
        self.setLoops(QMediaPlayer.Infinite)


class MediaSlider(QSlider):
    def __init__(self, media_player):
        super().__init__(Qt.Horizontal)
        self.media_player = media_player
        self.media_player.positionChanged.connect(self.setValue)
        self.is_mouse_pressed = False
        self.setRange(0, self.media_player.duration())
        self.setTickInterval(1000)
        self.setTickPosition(QSlider.TicksBelow)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouseMoveEvent(event)
        else:
            super().mousePressEvent(event)

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
            self.media_player.play()
        else:
            super().mouseReleaseEvent(event)

    """Override"""
    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.media_player.pause()
            slider_range = self.maximum() - self.minimum()
            click_position = event.position().x()
            slider_width = self.width()
            position = int(slider_range * click_position / slider_width)
            self.media_player.setPosition(position)
        else:
            super().mouseMoveEvent(event)


class MediaButtons(QWidget):
    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button = QPushButton("Reset")
        self.stop_button.clicked.connect(self.media_player.stop)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)


class VideoPreview(QWidget):
    """Main class holding all video preview widgets."""
    def __init__(self):
        super().__init__()
        self.media_player = MediaPlayer()
        # Has to be connected for the video to stretch properly once
        # it's loaded for the first time.
        self.media_player.video_output.nativeSizeChanged.connect(
            self.stretch_video_output
        )
        self.media_player.play()

        self.media_slider = MediaSlider(self.media_player)
        self.media_buttons = MediaButtons(self.media_player)

        self.scene = QGraphicsScene()
        self.scene.addItem(self.media_player.video_output)

        self.view = GraphicsView()
        self.view.setScene(self.scene)

        self.editing_timeline = TimelineWidget()

        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.media_buttons)
        self.layoutas.addWidget(self.media_slider)
        self.layoutas.addWidget(self.editing_timeline.view)

        self.setLayout(self.layoutas)

    @Slot()
    def stretch_video_output(self):
        """Stretch video output to fit the whole view."""
        self.view.fitInView(self.media_player.video_output, Qt.IgnoreAspectRatio)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Preview")
        self.setGeometry(100, 100, 800, 600)

        self.video_preview = VideoPreview()
        self.setCentralWidget(self.video_preview)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
