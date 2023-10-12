from PySide6.QtCore import Slot, QRectF
from PySide6.QtWidgets import QPushButton

from ._cropper import Cropper


class CropButton(QPushButton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.media_player = None
        self.cropper = None
        self.max_cropper_rect = None
        self.clicked.connect(self.__on_click)
        
    def set_media_player(self, media_player):
        self.media_player = media_player

    def set_max_cropper_rect(self, width, height):
        self.max_cropper_rect = QRectF(0, 0, width, height)
        self.__initialize_cropper()
    
    def __initialize_cropper(self):
        self.cropper = Cropper(self.media_player.scene, self.max_cropper_rect)
        self.cropper.hide()
        self.cropper.update()

    @Slot()
    def __on_click(self):
        if not self.cropper.isVisible():
            self.setChecked(True)
            self.cropper.show()
        else:
            self.setChecked(False)
            self.cropper.hide()
