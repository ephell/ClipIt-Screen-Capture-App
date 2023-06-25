from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaButtons(QWidget):

    def __init__(self, media_player):
        super().__init__()
        self.media_player = media_player
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.media_player.pause)
        self.stop_button = QPushButton("Reset")
        self.stop_button.clicked.connect(self.media_player.stop)
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.stop_button)
        self.setLayout(self.layout)
