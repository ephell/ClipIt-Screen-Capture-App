from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer

from ._audio_output import AudioOutput
from ._video_output import VideoOutput


class MediaPlayer(QMediaPlayer):

    def __init__(self, scene, file_path, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.file_path = file_path
        self.source_file = QUrl.fromLocalFile(self.file_path)
        self.setSource(self.source_file)
        self.audio_output = AudioOutput(self)
        self.setAudioOutput(self.audio_output)
        self.video_output = VideoOutput(self.scene)
        self.setVideoOutput(self.video_output)
        self.start_time = 0
        self.end_time = self.duration()

    def update_start_time(self, new_start_time):
        self.start_time = new_start_time

    def update_end_time(self, new_end_time):
        self.end_time = new_end_time

    """Override"""
    def stop(self):
        if self.playbackState() == QMediaPlayer.PlayingState:
            self.setPosition(self.start_time)
        else:
            super().stop()
            self.setPosition(self.start_time)

    """Override"""
    def play(self):
        if (
            self.playbackState() == QMediaPlayer.PausedState
            and self.position() >= self.end_time
        ):
            self.setPosition(self.start_time)
            super().play()
        else:
            super().play()
