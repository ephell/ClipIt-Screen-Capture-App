from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class TimelineItem(QGraphicsRectItem):
    def __init__(self, sceneRect):
        super().__init__()
        self.sceneWidth = sceneRect.width()
        self.sceneHeight = sceneRect.height()
        self.setFlag(QGraphicsRectItem.ItemIsMovable, True)
        self.setRect(0, 0, self.sceneWidth, self.sceneHeight/2)
        self.moveToMiddle()

    """Override"""
    def paint(self, painter, option, widget):
        painter.setPen(QPen(Qt.red))
        painter.setBrush(QBrush(Qt.red))
        painter.drawRect(self.rect())

    def moveToMiddle(self):
        item_height = self.rect().height()
        padding = (self.sceneHeight - item_height) / 2
        self.setPos(0, padding)


class TimelineScene(QGraphicsScene):
    def __init__(self, mediaDuration):
        super().__init__()
        if mediaDuration is not None:
            self.setSceneRect(0, 0, mediaDuration/10, 150)
        else:
            self.setSceneRect(0, 0, 150, 150)


class TimelineView(QGraphicsView):
    def __init__(self, scene=None):
        super().__init__()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setScene(scene)
        self.setFixedHeight(150)

    """Override"""
    def showEvent(self, event):
        super().showEvent(event)
        self.equalizeSceneAndViewDimensions()

    """Override"""
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.equalizeSceneAndViewDimensions()

    def equalizeSceneAndViewDimensions(self):
        self.scene().setSceneRect(0, 0, self.width(), self.height())


class MainWindow(QMainWindow):
    """For testing."""
    def __init__(self, mediaDuration=None):
        super().__init__()

        self.scene = TimelineScene(mediaDuration)
        self.view = TimelineView(self.scene)

        self.timeline_item = TimelineItem(self.scene.sceneRect())
        self.scene.addItem(self.timeline_item)

        self.setCentralWidget(self.view)


class LoadedMediaWidget(QWidget):
    """Main widget."""
    def __init__(self, mediaDuration=None):
        super().__init__()

        self.scene = TimelineScene(mediaDuration)
        self.view = TimelineView(self.scene)

        self.timeline_item = TimelineItem(self.scene.sceneRect())
        self.scene.addItem(self.timeline_item)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
