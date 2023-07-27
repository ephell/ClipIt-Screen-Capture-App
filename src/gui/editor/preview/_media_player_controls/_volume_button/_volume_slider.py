from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Qt


class VolumeSlider(QSlider):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setOrientation(Qt.Vertical)
        self.setRange(0, 100)
        self.setValue(100)
        self.setTickInterval(10)
        self.setPageStep(10)
        self.dragging = False

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.setValue(self.__calculate_new_slider_value(event))
        super().mousePressEvent(event)

    """Override"""
    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)

    """Override"""
    def mouseMoveEvent(self, event):
        if self.dragging:
            self.setValue(self.__calculate_new_slider_value(event))
        super().mouseMoveEvent(event)

    def __calculate_new_slider_value(self, event):
        slider_value_per_pixel  = (self.maximum() - self.minimum()) / self.height()
        click_pos_y = event.y()
        return self.maximum() - int(slider_value_per_pixel  * click_pos_y)
