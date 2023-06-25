from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *

from .preview.preview import Preview
from .timeline.timeline import Timeline


class Editor(QWidget):

    def __init__(self):
        super().__init__()

        self.preview = Preview()
        self.timeline = Timeline(self.preview.get_media_player())

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.timeline)
        self.setLayout(self.layout)
