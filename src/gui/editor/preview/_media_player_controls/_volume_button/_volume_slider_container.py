from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QDialog

from ._volume_slider import VolumeSlider


class VolumeSliderContainer(QDialog):
    
    def __init__(
            self, 
            button_position, 
            button_width, 
            button_height, 
            parent=None
        ):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.button_position = button_position
        self.button_width = button_width
        self.button_height = button_height
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.slider = VolumeSlider(self)
        self.layout.addWidget(self.slider)

    """Override"""
    def showEvent(self, event):
        self.update_position(
            self.button_position, 
            self.button_width, 
            self.button_height
        )
        super().showEvent(event)

    """Override"""
    def leaveEvent(self, event):
        if not self.isHidden():
            self.hide()

    def update_position(self, button_position, button_width, button_height):
        self.button_position = button_position
        self.button_width = button_width
        self.button_height = button_height
        slider_x = self.button_position.x() \
                   + (self.button_width - self.rect().width()) \
                   // 2
        slider_y = self.button_position.y() - self.rect().height()
        self.move(slider_x, slider_y)
