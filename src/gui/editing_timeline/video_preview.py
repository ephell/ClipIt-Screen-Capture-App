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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    player = QMediaPlayer()
    videoItem = QGraphicsVideoItem()
    player.setVideoOutput(videoItem)

    audioOutput = QAudioOutput()
    player.setAudioOutput(audioOutput)

    scene = QGraphicsScene()
    scene.addItem(videoItem)

    view = VideoGraphicsView(scene)
    view.resize(800, 600)
    view.show()

    player.setSource(QUrl("src/gui/editing_timeline/test.mp4"))
    player.setLoops(QMediaPlayer.Infinite)
    player.play()

    # Set the initial size of the video item to match the size of the QGraphicsView
    videoItem.setSize(view.size())

    sys.exit(app.exec())
