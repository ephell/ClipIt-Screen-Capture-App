from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaSlider(QSlider):
    
    def __init__(self, media_player):
        super().__init__(Qt.Horizontal)
        self.media_player = media_player
        self.media_player.positionChanged.connect(self.setValue)
        self.is_mouse_pressed = False
        self.setRange(0, self.media_player.duration())
        self.setTickInterval(1000)
        self.setTickPosition(QSlider.TicksBelow)

    """Override"""
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = True
            self.mouseMoveEvent(event)
        else:
            super().mousePressEvent(event)

    """Override"""
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_mouse_pressed = False
            self.media_player.play()
        else:
            super().mouseReleaseEvent(event)

    """Override"""
    def mouseMoveEvent(self, event):
        if self.is_mouse_pressed:
            self.media_player.pause()
            slider_range = self.maximum() - self.minimum()
            click_position = event.position().x()
            slider_width = self.width()
            position = int(slider_range * click_position / slider_width)
            self.media_player.setPosition(position)
        else:
            super().mouseMoveEvent(event)
