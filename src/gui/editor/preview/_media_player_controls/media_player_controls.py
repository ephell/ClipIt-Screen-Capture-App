from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from .Ui_MediaPlayerControls import Ui_MediaPlayerControls


class MediaPlayerControls(Ui_MediaPlayerControls, QWidget):

    def __init__(self, media_player, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.media_player = media_player
        self.render_and_save_button.set_media_player(self.media_player)
        if not self.media_player.hasAudio():
            self.volume_button.setEnabled(False)
        self.__connect_signals_and_slots()

    def __connect_signals_and_slots(self):
        self.play_button.clicked.connect(self.media_player.play)
        self.pause_button.clicked.connect(self.media_player.pause)
        self.reset_button.clicked.connect(self.media_player.stop)
        self.render_and_save_button.clicked.connect(
            self.render_and_save_button.on_click
        )
        self.volume_button.volume_slider_container.slider.valueChanged.connect(
            self.__on_volume_slider_value_changed
        )
        
    @Slot()
    def __on_volume_slider_value_changed(self, value):
        self.media_player.audio_output.setVolume(value / 100.0)
