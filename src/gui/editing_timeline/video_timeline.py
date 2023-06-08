import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editing Timeline")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self.central_widget)
        self.label.setText("TIMELINE")
        self.central_layout.addWidget(self.label)

        self.view = QGraphicsView()
        self.scene = QGraphicsScene()

        self.view.setSceneRect(0, 0, 800, 600)

        self.view.setScene(self.scene)
        self.central_layout.addWidget(self.view)

        self.g_item_1 = RectangleItem(QRectF(0, 0, 250, 50), Qt.red)
        self.g_item_2 = RectangleItem(QRectF(0, 0, 250, 50), Qt.blue)

        self.layout = QGraphicsGridLayout()
        self.layout.addItem(self.g_item_1, 0, 0)
        self.layout.addItem(self.g_item_2, 1, 0)

        self.panel_widget = QGraphicsWidget()
        self.panel_widget.setLayout(self.layout)

        self.scene.addItem(self.panel_widget)


class RectangleItem(QGraphicsWidget):
    def __init__(self, rect, color):
        super().__init__()
        self.rect = rect
        self.color = color

    """Override"""
    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self.rect)

    """Override"""
    def boundingRect(self):
        return self.rect
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
