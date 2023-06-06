import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class HorizontalDragPixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def mouseMoveEvent(self, event):
        delta = event.scenePos() - event.lastScenePos()
        self.setPos(self.pos().x() + delta.x(), self.pos().y())


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.setWindowTitle("My App")
        self.setGeometry(400, 100, 1000, 800)
        self.app = app

        # Create a QGraphicsScene
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 214)  # Set the desired size

        self.scene2 = QGraphicsScene()
        self.scene2.setSceneRect(0, 0, 600, 214)  # Set the desired size
        

        # Add items to the scene
        self.scene.addItem(self.add_PixmapItem())
        self.scene2.addItem(self.add_PixmapItem())
        # self.add_PolygonItem()
        # self.add_RectItem(0, 0, 100, 100)
        # self.add_EllipseItem(50, 50, 100, 100)
        # self.add_TextItem("Hello World")
        # self.add_LineItem(0, 0, 100, 100)

        # Create a graphics view and set its size policy
        graphicView = QGraphicsView()
        graphicView.setScene(self.scene)
        graphicView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        graphicView2 = QGraphicsView()
        graphicView2.setScene(self.scene2)
        graphicView2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add the graphics view to the layout
        layout = QGridLayout()
        layout.addWidget(graphicView, 0, 0)
        layout.addWidget(graphicView2, 1, 0)

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(layout)

        # Set the container as the central widget
        self.setCentralWidget(container)

    def add_PixmapItem(self):
        pixmapItem = HorizontalDragPixmapItem(QPixmap("src/image.png"))
        return pixmapItem

    def add_PolygonItem(self):
        polygonItem = QGraphicsPolygonItem(
            QPolygonF(
                [QPointF(57, 0), QPointF(125, 0), 
                 QPointF(100, 125), QPointF(0, 100)]
            )
        )
        self.scene.addItem(polygonItem)
        polygonItem.setFlag(QGraphicsItem.ItemIsMovable)
        polygonItem.setBrush(self.get_brush(Qt.yellow))
        polygonItem.setPen(self.get_pen(Qt.yellow))

    def add_RectItem(self, x, y, width, height):
        rectItem = QGraphicsRectItem(x, y, width, height)
        self.scene.addItem(rectItem)
        rectItem.setFlag(QGraphicsItem.ItemIsMovable)
        rectItem.setBrush(self.get_brush(Qt.green))
        rectItem.setPen(self.get_pen(Qt.green))

    def add_EllipseItem(self, x, y, width, height):
        ellipseItem = QGraphicsEllipseItem(x, y, width, height)
        self.scene.addItem(ellipseItem)
        ellipseItem.setFlag(QGraphicsItem.ItemIsMovable)
        ellipseItem.setBrush(self.get_brush(Qt.red))
        ellipseItem.setPen(self.get_pen(Qt.red))

    def add_LineItem(self, x1, y1, x2, y2):
        lineItem = QGraphicsLineItem(x1, y1, x2, y2)
        self.scene.addItem(lineItem)
        lineItem.setFlag(QGraphicsItem.ItemIsMovable)
        lineItem.setPen(self.get_pen(Qt.blue))

    def add_TextItem(self, text):
        textItem = QGraphicsTextItem(text)
        self.scene.addItem(textItem)
        textItem.setFlag(QGraphicsItem.ItemIsMovable)
        textItem.setDefaultTextColor(Qt.black)

    def get_brush(self, color):
        return QBrush(color)
    
    def get_pen(self, color):
        return QPen(color)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec())
