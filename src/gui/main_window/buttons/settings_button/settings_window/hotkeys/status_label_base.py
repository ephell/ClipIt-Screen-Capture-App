from abc import abstractmethod

from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QColor

from src.settings.settings import Settings


class StatusLabelBase(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)        
        self.setFixedSize(10, 10)

    def set_state_normal(self):
        self.__set_color(QColor("green"), self.width() // 2)

    def set_state_pending(self):
        self.__set_color(QColor("yellow"), self.width() // 2)

    def set_state_error(self):
        self.__set_color(QColor("red"), self.width() // 2)

    @abstractmethod
    def set_initial_state(self):
        pass

    def __set_color(self, color, border_radius=None):
        style_sheet = f"background-color: {color.name()};"
        if border_radius is not None:
            style_sheet += f" border-radius: {border_radius}px;"
        self.setStyleSheet(style_sheet)
