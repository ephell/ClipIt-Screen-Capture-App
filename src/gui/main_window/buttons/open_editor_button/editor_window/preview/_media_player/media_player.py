from PySide6.QtCore import QUrl, Slot, Signal
from PySide6.QtMultimedia import QMediaPlayer

from ._audio_output import AudioOutput
from ._video_output import VideoOutput


class MediaPlayer(QMediaPlayer):

    finished_collecting_media_item_thumbnail_frames = Signal(list)

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
        # Related to logic of media item thumbnail frames collection.
        self.__video_sink = self.videoSink()
        self.__have_media_item_thumbnail_frames_been_collected = False
        self.__finished_collecting_signal_sent = False
        self.__captured_frame_count = 0
        self.__required_frame_count = 5
        self.__frames = []
        self.__frame_step_size = 100
        self.__frame_timestamps = self.__calculate_thumbnail_frame_timestamps()
        self.__video_sink.videoFrameChanged.connect(self.__on_video_frame_changed)

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

    @Slot()
    def __on_video_frame_changed(self, frame):
        if not self.__have_media_item_thumbnail_frames_been_collected:
            self.__collect_frame(frame)
        elif not self.__finished_collecting_signal_sent:
            self.finished_collecting_media_item_thumbnail_frames.emit(self.__frames)
            self.__finished_collecting_signal_sent = True

    def __collect_frame(self, frame):
        if (
            self.__captured_frame_count == 0 
            or frame.startTime() != self.__frames[-1].startTime()
        ):
            self.__frames.append(frame)
            self.__captured_frame_count += 1
            if self.__captured_frame_count < self.__required_frame_count:
                self.setPosition(self.__frame_timestamps[self.__captured_frame_count])
                return
        elif self.position() == self.duration():
            self.__captured_frame_count = self.__required_frame_count
        else:
            self.setPosition(self.position() + self.__frame_step_size)
        
        if self.__captured_frame_count == self.__required_frame_count:
            self.__have_media_item_thumbnail_frames_been_collected = True
            self.setPosition(0)

    def __calculate_thumbnail_frame_timestamps(self):
        interval = int(self.duration() / self.__required_frame_count)
        return [i * interval for i in range(self.__required_frame_count)]
