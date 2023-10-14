from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QColor


class StatusLabelBase(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)        
        self.setFixedSize(10, 10)
        self.__set_initial_color()

    def set_color(self, color, border_radius=None):
        style_sheet = f"background-color: {color.name()};"
        if border_radius is not None:
            style_sheet += f" border-radius: {border_radius}px;"
        self.setStyleSheet(style_sheet)

    def __set_initial_color(self):
        self.set_color(QColor("red"), self.width() // 2)
