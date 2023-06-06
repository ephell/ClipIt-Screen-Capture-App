import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtCore import QUrl
from PySide6.QtMultimediaWidgets import QGraphicsVideoItem

if __name__ == "__main__":
    app = QApplication(sys.argv)

    player = QMediaPlayer()
    videoItem = QGraphicsVideoItem()
    player.setVideoOutput(videoItem)


    scene = QGraphicsScene()
    scene.addItem(videoItem)
    view = QGraphicsView(scene)
    view.show()

    player.setSource(QUrl("src/test.mp4"))
    player.play()

    sys.exit(app.exec())
