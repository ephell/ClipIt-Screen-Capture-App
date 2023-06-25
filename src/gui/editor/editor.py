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
        self.timeline = Timeline(self.preview.media_player.duration())

        self.timeline.scene.ruler_handle_time_changed.connect(
            self.update_media_player_position
        )
        self.preview.media_player.positionChanged.connect(
            self.update_ruler_handle_position
        )
        self.preview.media_player.positionChanged.connect(
            self.pause_on_reaching_media_end_time
        )


        self.layout = QVBoxLayout()
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.timeline)
        self.setLayout(self.layout)

    @Slot()
    def update_media_player_position(self, time_ms):
        self.preview.media_player.setPosition(time_ms)

    @Slot()
    def update_ruler_handle_position(self, time_ms):
        self.timeline.ruler.ruler_handle.on_media_player_position_changed(
            time_ms
        )

    @Slot()
    def pause_on_reaching_media_end_time(self, current_time):
        end_time = self.timeline.media_item.end_time
        if current_time >= end_time:
            self.preview.media_player.setPosition(end_time)
            self.preview.media_player.pause()
