from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QDialog

from ._resolution_label import ResolutionLabel


class ResolutionLabelContainer(QDialog):
    
    def __init__(
            self, 
            crop_button_position, 
            crop_button_width, 
            crop_button_height, 
            parent=None
        ):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.crop_button_position = crop_button_position
        self.crop_button_width = crop_button_width
        self.crop_button_height = crop_button_height
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.resolution_label = ResolutionLabel(self)
        self.layout.addWidget(self.resolution_label)

    def update_position(self, crop_button_position, crop_button_width, crop_button_height):
        self.crop_button_position = crop_button_position
        self.crop_button_width = crop_button_width
        self.crop_button_height = crop_button_height
        new_x = self.crop_button_position.x() \
                + (self.crop_button_width - self.rect().width()) \
                // 2
        new_y = self.crop_button_position.y() - self.rect().height()
        self.move(new_x, new_y)

    """Override"""
    def showEvent(self, event):
        self.update_position(
            self.crop_button_position, 
            self.crop_button_width, 
            self.crop_button_height
        )
        super().showEvent(event)
