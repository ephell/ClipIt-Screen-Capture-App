from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QDialog

from ._resolution_label import ResolutionLabel


class ResolutionLabelContainer(QDialog):
    
    def __init__(
            self, 
            button_position, 
            button_width, 
            button_height, 
            parent=None
        ):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.button_position = button_position
        self.button_width = button_width
        self.button_height = button_height
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.resolution_label = ResolutionLabel(self)
        self.layout.addWidget(self.resolution_label)

    def update_position(self, button_position, button_width, button_height):
        self.button_position = button_position
        self.button_width = button_width
        self.button_height = button_height
        new_x = self.button_position.x() \
                + (self.button_width - self.rect().width()) \
                // 2
        new_y = self.button_position.y() - self.rect().height()
        self.move(new_x, new_y)

    """Override"""
    def showEvent(self, event):
        self.update_position(
            self.button_position, 
            self.button_width, 
            self.button_height
        )
        super().showEvent(event)
