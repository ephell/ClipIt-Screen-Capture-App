from PySide6.QtCore import Slot, QRect
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QPushButton

from ._volume_slider_container import VolumeSliderContainer


class VolumeButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.volume_slider_container = VolumeSliderContainer(
            self.__get_position(),
            self.__get_width(),
            self.__get_height(),
            self.parent()
        )
        self.clicked.connect(self.on_click)

    """Override"""
    def showEvent(self, event):
        self.volume_slider_container.update_position(
            self.__get_position(), 
            self.__get_width(),
            self.__get_height()
        )
        super().showEvent(event)

    """Override"""
    def leaveEvent(self, event):
        local_container_rect = self.volume_slider_container.rect()
        global_top_left = self.volume_slider_container.mapToGlobal(
            local_container_rect.topLeft()
        )
        global_bottom_right = self.volume_slider_container.mapToGlobal(
            local_container_rect.bottomRight()
        )
        global_container_rect = QRect(global_top_left, global_bottom_right)
        global_cursor_pos = QCursor.pos()
        if not global_container_rect.contains(global_cursor_pos):
            self.volume_slider_container.hide()

    @Slot()
    def on_click(self):
        if self.volume_slider_container.isHidden():
            self.volume_slider_container.show()
        else:
            self.volume_slider_container.hide()

    @Slot()
    def on_editor_position_changed(self):
        self.volume_slider_container.update_position(
            self.__get_position(),
            self.__get_width(),
            self.__get_height()
        )

    @Slot()
    def on_editor_resized(self):
        self.volume_slider_container.update_position(
            self.__get_position(),
            self.__get_width(),
            self.__get_height()
        )

    def __get_position(self):
        return self.mapToGlobal(self.rect().topLeft())
    
    def __get_width(self):
        return self.width()
    
    def __get_height(self):
        return self.height()
