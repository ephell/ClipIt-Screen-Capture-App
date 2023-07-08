import mss
import numpy as np
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QBrush, QPen, QPixmap, QImage, QColor, QRegion
from PySide6.QtWidgets import QWidget


class AreaSelector(QWidget):
    
    def __init__(self, get_area_coords_callback):
        super().__init__()
        self.get_area_coords_callback = get_area_coords_callback
        self.dragging = False
        self.start_pos = None
        self.end_pos = None
        self.screenshot = self.__take_screenshot()
        self.setFixedSize(self.screenshot.width(), self.screenshot.height())
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.ToolTip)

    """Override"""
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Wating prevents the right-click menu from appearing.
            QTimer.singleShot(100, self.close)
        elif event.button() == Qt.LeftButton:
            self.dragging = True
            self.start_pos = event.position()
            self.end_pos = event.position()
            self.update()

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.end_pos = event.position()
            self.get_area_coords_callback(
                min(self.start_pos.x(), self.end_pos.x()),
                min(self.start_pos.y(), self.end_pos.y()),
                max(self.start_pos.x(), self.end_pos.x()),
                max(self.start_pos.y(), self.end_pos.y())
            )

    """Override"""
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.end_pos = event.position()
            self.update()

    """Override"""
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the screenshot
        painter.drawPixmap(self.rect(), self.screenshot)

        # Region that will be drawn around the selected area (rectangle)
        dimmed_region = QRegion(self.rect())

        # Draw the rectangle
        if self.start_pos is not None and self.end_pos is not None:
            rectangle = QRect(*self.__get_rectangle())
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

    def __take_screenshot(self):
        with mss.mss() as sct:
            sc = sct.grab({
                'top': 0, 
                'left': 0, 
                'width': sct.monitors[0]["width"], 
                'height': sct.monitors[0]["height"]
            })

        # Remove alpha channel and convert to RGB
        sc_bgra = np.frombuffer(sc.bgra, dtype=np.uint8)
        sc_bgr = sc_bgra.reshape((sc.height, sc.width, 4))
        sc_bgr = np.delete(sc_bgr, 3, axis=2)
        sc_rgb = sc_bgr[...,::-1]
        sc_rgb = np.ascontiguousarray(sc_rgb)

        q_image = QImage(
            sc_rgb,
            sc.width,
            sc.height,
            QImage.Format_RGB888,
        )

        return QPixmap.fromImage(q_image)

    def __get_rectangle(self):
        x1, y1 = self.start_pos.x(), self.start_pos.y()
        x2, y2 = self.end_pos.x(), self.end_pos.y()

        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x1 - x2)
        h = abs(y1 - y2)

        return x, y, w, h
