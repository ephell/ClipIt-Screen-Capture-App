import mss
import numpy as np
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QPainter, QBrush, QPen, QPixmap, QImage, QColor, QRegion
from PySide6.QtWidgets import QWidget


class AreaSelector(QWidget):
    
    def __init__(self, get_area_coords_callback, parent=None):
        super().__init__(parent)
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

            top_x = min(self.start_pos.x(), self.end_pos.x())
            top_y = min(self.start_pos.y(), self.end_pos.y())
            bottom_x = max(self.start_pos.x(), self.end_pos.x())
            bottom_y = max(self.start_pos.y(), self.end_pos.y())

            # Get whole area of the monitor if 1 click was made without dragging
            if bottom_x - top_x < 1 or bottom_y - top_y < 1:
                monitor_index = self.__get_monitor_by_point(top_x, top_y)
                top_x, top_y, bottom_x, bottom_y = self.__get_monitor_coords_by_index(monitor_index)

            self.get_area_coords_callback(top_x, top_y, bottom_x, bottom_y)

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

    def __get_monitor_by_point(self, x, y):
        """Get the index of the monitor that contains the point (x, y)."""
        with mss.mss() as sct:
            monitors = sct.monitors
            for i in range(1, len(monitors)):
                m = monitors[i]
                if (m["left"] <= x < m["left"] + m["width"] 
                    and m["top"] <= y < m["top"] + m["height"]):
                    return i
            return None

    def __get_monitor_coords_by_index(self, monitor_index):
        with mss.mss() as sct:
            monitor = sct.monitors[monitor_index]
            top_left_x = monitor["left"]
            top_left_y = monitor["top"]
            bottom_right_x = monitor["left"] + monitor["width"]
            bottom_right_y = monitor["top"] + monitor["height"]
            return (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
