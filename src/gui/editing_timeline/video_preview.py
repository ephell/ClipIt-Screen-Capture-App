import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class VideoGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)


class MediaPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self.video_item = QGraphicsVideoItem()
        self.setVideoOutput(self.video_item)
        self.audio_output = QAudioOutput()
        self.setAudioOutput(self.audio_output)
        self.setSource(QUrl("src/gui/editing_timeline/test.mp4"))
        self.setLoops(QMediaPlayer.Infinite)


class PlaybackSlider(QSlider):
    def __init__(self, mediaPlayer):
        super().__init__(Qt.Horizontal)
        self.mediaPlayer = mediaPlayer
        self.mediaPlayer.positionChanged.connect(self.setValue)
        self.mousePressed = False
        self.setRange(0, self.mediaPlayer.duration())
        self.setTickInterval(1000)
        self.setTickPosition(QSlider.TicksBelow)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed = True
            self.mouseMoveEvent(event)
        else:
            super().mousePressEvent(event)

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePressed = False
            self.mediaPlayer.play()
        else:
            super().mouseReleaseEvent(event)

    """Override"""
    def mouseMoveEvent(self, event):
        if self.mousePressed:
            self.mediaPlayer.pause()
            slider_range = self.maximum() - self.minimum()
            click_position = event.position().x()
            slider_width = self.width()
            position = int(slider_range * click_position / slider_width)
            self.mediaPlayer.setPosition(position)
        else:
            super().mouseMoveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Preview")

        self.player = MediaPlayer()

        self.scene = QGraphicsScene()
        self.scene.addItem(self.player.video_item)

        self.view = VideoGraphicsView(self.scene)
        self.view.resize(800, 600)

        self.player.video_item.setSize(self.view.size())

        self.playbackSlider = PlaybackSlider(self.player)
        
        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.playbackSlider)

        self.container = QWidget()
        self.container.setLayout(self.layoutas)

        self.setCentralWidget(self.container)
        self.player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
