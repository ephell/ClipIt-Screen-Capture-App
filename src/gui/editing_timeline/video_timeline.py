from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TimelineItem(QGraphicsRectItem):
    def __init__(self, view, duration):
        super().__init__()
        self.view = view
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.resizeBasedOnDuration(self.view.height(), duration)

    def resizeBasedOnDuration(self, height, duration):
        scene_width = self.view.width()
        duration_sec = duration / 1000
        item_width = scene_width * duration_sec / 10
        self.setRect(0, 0, item_width, height - 50)

    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red))
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(self.rect())


class TimelineScene(QGraphicsScene):
    def __init__(self):
        super().__init__()


class TimelineView(QGraphicsView):
    def __init__(self, scene=None):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setScene(scene)
        self.setFixedHeight(150)


class LoadedMediaWidget(QWidget):
    """Main widget."""
    def __init__(self, mediaDuration):
        super().__init__()

        self.scene = TimelineScene()
        self.view = TimelineView(self.scene)

        self.timeline_item = TimelineItem(self.view, mediaDuration)
        self.scene.addItem(self.timeline_item)


class MainWindow(QMainWindow):
    """For testing."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        self.scene = TimelineScene()
        self.view = TimelineView(self.scene)

        self.timeline_item = TimelineItem(self.view, 5000)
        self.scene.addItem(self.timeline_item)

        self.setCentralWidget(self.view)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
