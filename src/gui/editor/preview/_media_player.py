from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import *
from PySide6.QtMultimediaWidgets import *


class MediaPlayer(QMediaPlayer):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setSource(QUrl("src/gui/editor/test.mp4"))
        # self.setLoops(QMediaPlayer.Infinite)
        self.video_output = _VideoOutput(self.scene)
        self.setVideoOutput(self.video_output)
        # self.audio_output = _AudioOutput()
        # self.setAudioOutput(self.audio_output)


class _VideoOutput(QGraphicsVideoItem):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.scene.addItem(self)


class _AudioOutput(QAudioOutput):

    def __init__(self):
        super().__init__()
        self.setMuted(True)
