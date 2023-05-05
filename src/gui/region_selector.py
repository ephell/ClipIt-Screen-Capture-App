import mss
from PIL import Image
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QBrush, QPen, QPixmap, QImage, QColor, QRegion
from PySide6.QtWidgets import QWidget


class RegionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.ToolTip
        )
        self.initUI()

    def initUI(self):
        self.screenshot = self.take_screenshot()
        self.setFixedSize(self.screenshot.width(), self.screenshot.height())
        self.dragging = False
        self.startPos = None
        self.endPos = None

    def take_screenshot(self):
        with mss.mss() as sct:
            screenshot = Image.open(sct.shot(mon=-1))

        q_image = QImage(
            screenshot.tobytes(),
            screenshot.width,
            screenshot.height,
            QImage.Format_RGB888,
        )

        return QPixmap.fromImage(q_image)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Prevents the right-click menu from appearing.
            QTimer.singleShot(100, self.close)
        elif event.button() == Qt.LeftButton:
            self.dragging = True
            self.startPos = event.position()
            self.endPos = event.position()
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.endPos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.endPos = event.position()
            self.update()
            print(f"Rectangle: {self.getRect()}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the screenshot
        painter.drawPixmap(self.rect(), self.screenshot)

        # Region that will be drawn around the selected area (rectangle)
        dimmed_region = QRegion(self.rect())

        # Draw the rectangle
        if self.startPos is not None and self.endPos is not None:
            rectangle = QRect(*self.getRect())
            pen = QPen(Qt.white, 1)
            pen.setStyle(Qt.DashLine)
            pen.setDashPattern([5, 5])
            painter.setPen(pen)
            painter.drawRect(rectangle)

            # Subtract the rectangle region from the whole region
            rectangle_region = QRegion(rectangle)
            dimmed_region = dimmed_region.subtracted(rectangle_region)

        # Draw semi-transparent black rectangle around the selected area
        painter.setClipRegion(dimmed_region)
        painter.fillRect(self.rect(), QBrush(QColor(0, 0, 0, 128)))

    def getRect(self):
        x1, y1 = self.startPos.x(), self.startPos.y()
        x2, y2 = self.endPos.x(), self.endPos.y()

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)

        return x, y, w, h
