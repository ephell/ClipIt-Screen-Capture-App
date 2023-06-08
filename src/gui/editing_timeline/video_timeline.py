from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TimelineItem(QGraphicsRectItem):
    def __init__(self, height):
        super().__init__()
        self.setRect(0, 0, 150, height-25)
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")

        self.scene = TimelineScene()
        self.view = TimelineView(self.scene)

        self.timeline_item = TimelineItem(self.view.height())
        self.scene.addItem(self.timeline_item)

        self.setCentralWidget(self.view)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
