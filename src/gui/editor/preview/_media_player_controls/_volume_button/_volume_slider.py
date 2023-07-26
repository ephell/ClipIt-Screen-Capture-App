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
