from PySide6.QtCore import Slot
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
    def moveEvent(self, event):
        self.volume_slider_container.update_position(
            self.__get_position(),
            self.__get_width(),
            self.__get_height()
        )
        super().moveEvent(event)

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

    def __get_position(self):
        return self.mapToGlobal(self.rect().topLeft())
    
    def __get_width(self):
        return self.width()
    
    def __get_height(self):
        return self.height()
