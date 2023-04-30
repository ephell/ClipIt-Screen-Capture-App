import datetime
import multiprocessing as mp
import os

from encoder import Encoder
from recorder_loopback import LoopbackRecorder
from recorder_microphone import MicrophoneRecorder
from recorder_video import VideoRecorder
from utils_audio import AudioUtils


class Recorder:
    """Recording controller."""

    def __init__(
            self,
            duration, 
            record_video,
            record_loopback,
            record_microphone,
            **kwargs
        ):
        self.duration = duration
        self.record_video = record_video
        self.record_loopback = record_loopback
        self.record_microphone = record_microphone
        self.__unpack_kwargs(kwargs)
        self.video_recorder = None
        self.loopback_recorder = None
        self.microphone_recorder = None

        if self.record_video:
            self.__initialize_video_recorder()
        if self.record_loopback:
            self.__initialize_loopback_recorder()
        if self.record_microphone:
            self.__initialize_microphone_recorder()

        # Make sure all recorders start at the same time.
        barrier = mp.Barrier(len(self.__get_recorders()))
        for recorder in self.__get_recorders():
            recorder.barrier = barrier

    def record(self):
        for recorder in self.__get_recorders():
            recorder.start()
        for recorder in self.__get_recorders():
            recorder.join()
        self.__generate_final_video()
        self.__clean_up_temp_directory()

    def __unpack_kwargs(self, kwargs):
        self.monitor = kwargs.get("monitor", 1)
        self.region = kwargs.get("region", [0, 0, 1920, 1080])
        self.fps = kwargs.get("fps", 30)

    def __initialize_video_recorder(self):
        if self.record_video:
            self.video_recorder = VideoRecorder(
                monitor=self.monitor, 
                region=self.region,
                duration=self.duration,
                fps=self.fps,
            )

    def __initialize_loopback_recorder(self):
        loopback_device = AudioUtils.get_default_loopback_device()
        if loopback_device is not None:
            self.record_loopback = True
            self.loopback_recorder = LoopbackRecorder(
                loopback_device=loopback_device,
                duration=self.duration,
            )
        else:
            self.record_loopback = False

    def __initialize_microphone_recorder(self):
        microphone = AudioUtils.get_default_microphone()
        if microphone is not None:
            self.record_microphone = True
            self.microphone_recorder = MicrophoneRecorder(
                microphone=microphone,
                duration=self.duration,
            )
        else:
            self.record_microphone = False

    def __get_recorders(self):
        recorders = [
            self.video_recorder, 
            self.loopback_recorder, 
            self.microphone_recorder
        ]
        return [recorder for recorder in recorders if recorder is not None]

    def __generate_final_video(self):
        """Generates the final file from recorded temporary files."""
        if self.record_loopback and self.record_microphone:
            Encoder.merge_audio(
                first_clip="temp/TEMP-loopback.wav", 
                second_clip="temp/TEMP-microphone.wav", 
                output_path="temp/TEMP-merged.wav"
            )
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-merged.wav"
            )
        elif self.record_loopback and not self.record_microphone:
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-loopback.wav"
            )
        elif self.record_microphone and not self.record_loopback:
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-microphone.wav"
            )
        else:
            os.replace("temp/TEMP-video.mp4", "temp/TEMP-Final.mp4")

        # Rename the final file and move it to output folder.
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        filename = f"{timestamp}.mp4"
        os.rename("temp/TEMP-Final.mp4", f"recordings/{filename}")

    def __clean_up_temp_directory(self):
        """Removes all temporary files from the temp directory."""
        files = os.listdir("temp/")
        for file in files:
            if "TEMP-" in file:
                os.remove("temp/" + file)
