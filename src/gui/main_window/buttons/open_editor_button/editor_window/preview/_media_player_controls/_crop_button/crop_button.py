from PySide6.QtCore import Slot, QRectF
from PySide6.QtWidgets import QPushButton

from ._cropper import Cropper
from ._resolution_label_container import ResolutionLabelContainer


class CropButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_player = None
        self.cropper = None
        self.max_cropper_rect = None
        self.resolution_label_container = ResolutionLabelContainer(
            self.__get_position(),
            self.__get_width(),
            self.__get_height(),
            self.parent()
        )
        self.clicked.connect(self.__on_click)
    
    """Override"""
    def showEvent(self, event):
        self.resolution_label_container.update_position(
            self.__get_position(), 
            self.__get_width(),
            self.__get_height()
        )
        super().showEvent(event)

    def set_media_player(self, media_player):
        self.media_player = media_player

    def set_max_cropper_rect(self, width, height):
        self.max_cropper_rect = QRectF(0, 0, width, height)
        self.__initialize_cropper()
    
    def __initialize_cropper(self):
        self.cropper = Cropper(self.media_player.scene, self.max_cropper_rect)
        self.cropper.hide()
        self.cropper.update()

    def __get_position(self):
        return self.mapToGlobal(self.rect().topLeft())
    
    def __get_width(self):
        return self.width()
    
    def __get_height(self):
        return self.height()

    @Slot()
    def __on_click(self):
        if not self.cropper.isVisible():
            self.setChecked(True)
            self.cropper.show()
            self.resolution_label_container.show()
        else:
            self.setChecked(False)
            self.cropper.hide()
            self.resolution_label_container.hide()

    @Slot()
    def on_editor_position_changed(self):
        self.resolution_label_container.update_position(
            self.__get_position(),
            self.__get_width(),
            self.__get_height()
        )

    @Slot()
    def on_editor_resized(self):
        self.resolution_label_container.update_position(
            self.__get_position(),
            self.__get_width(),
            self.__get_height()
        )
