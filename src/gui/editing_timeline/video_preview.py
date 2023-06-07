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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Preview")

        self.player = MediaPlayer()

        self.scene = QGraphicsScene()
        self.scene.addItem(self.player.video_item)

        self.view = VideoGraphicsView(self.scene)
        self.view.resize(800, 600)

        # Set the initial size of the video item to match QGraphicsView
        self.player.video_item.setSize(self.view.size())
        self.player.play()

        self.setCentralWidget(self.view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
