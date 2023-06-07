import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


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
        self.audio_output = QAudioOutput()
        self.setAudioOutput(self.audio_output)
        self.setSource(QUrl("src/gui/editing_timeline/test.mp4"))
        self.setLoops(QMediaPlayer.Infinite)


class MediaSlider(QSlider):
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


class VideoPreview(QWidget):
    """Main class holding all video preview widgets."""
    def __init__(self):
        super().__init__()
        self.mediaPlayer = MediaPlayer()
        self.mediaPlayer.video_output.nativeSizeChanged.connect(self.stretchVOutput)
        self.mediaPlayer.play()

        self.mediaSlider = MediaSlider(self.mediaPlayer)

        self.scene = QGraphicsScene()
        self.scene.addItem(self.mediaPlayer.video_output)

        self.view = GraphicsView()
        self.view.setScene(self.scene)

        self.layoutas = QVBoxLayout()
        self.layoutas.addWidget(self.view)
        self.layoutas.addWidget(self.mediaSlider)
        self.setLayout(self.layoutas)

    @Slot()
    def stretchVOutput(self):
        """Stretch video output to fit the whole view."""
        self.view.fitInView(self.mediaPlayer.video_output, Qt.IgnoreAspectRatio)


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
