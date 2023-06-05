from logger import GlobalLogger
log = GlobalLogger.LOGGER

import datetime
import multiprocessing as mp
import os
import threading

from encoder import Encoder
from recorder.recorder_loopback import LoopbackRecorder
from recorder.recorder_microphone import MicrophoneRecorder
from recorder.recorder_video import VideoRecorder
from settings import Paths, TempFiles
from utilities.audio import AudioUtils


class Recorder(threading.Thread):
    """Recording controller."""

    def __init__(
            self,
            record_video,
            record_loopback,
            record_microphone,
            stop_event=None,
            **kwargs
        ):
        super().__init__()
        self.record_video = record_video
        self.record_loopback = record_loopback
        self.record_microphone = record_microphone
        self.stop_event = stop_event
        self.__unpack_kwargs(kwargs)
        self.video_recorder = None
        self.loopback_recorder = None
        self.microphone_recorder = None
        self.video_recorder_stop_event = None
        self.loopback_recorder_stop_event = None
        self.microphone_recorder_stop_event = None
    
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

    def run(self):
        for recorder in self.__get_recorders():
            recorder.start()

        self.stop_event.wait()

        for recorder in self.__get_recorders():
            recorder.stop_event.set()

        for recorder in self.__get_recorders():
            recorder.join()

        self.__generate_final_video()
        self.__clean_up_temp_directory()
        self.is_recording_callback(False)
        log.info("All done!")

    def __unpack_kwargs(self, kwargs):
        self.region = kwargs.get("region")
        self.monitor = kwargs.get("monitor")
        self.fps = kwargs.get("fps")
        self.is_recording_callback = kwargs.get("is_recording_callback")

    def __initialize_video_recorder(self):
        self.video_recorder_stop_event = mp.Event()
        self.video_recorder = VideoRecorder(
            region=self.region,
            monitor=self.monitor,
            fps=self.fps,
            stop_event=self.video_recorder_stop_event
        )

    def __initialize_loopback_recorder(self):
        loopback_device = AudioUtils.get_default_loopback_device()
        if loopback_device is not None:
            self.record_loopback = True
            self.loopback_recorder_stop_event = mp.Event()
            self.loopback_recorder = LoopbackRecorder(
                loopback_device=loopback_device,
                stop_event=self.loopback_recorder_stop_event
            )
        else:
            self.record_loopback = False

    def __initialize_microphone_recorder(self):
        microphone = AudioUtils.get_default_microphone()
        if microphone is not None:
            self.record_microphone = True
            self.microphone_recorder_stop_event = mp.Event()
            self.microphone_recorder = MicrophoneRecorder(
                microphone=microphone,
                stop_event=self.microphone_recorder_stop_event
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
                first_clip=f"{Paths.TEMP_DIR}/{TempFiles.LOOPBACK_AUDIO_FILE}", 
                second_clip=f"{Paths.TEMP_DIR}/{TempFiles.MICROPHONE_AUDIO_FILE}",
            )
            Encoder.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.MERGED_AUDIO_FILE}"
            )
        elif self.record_loopback and not self.record_microphone:
            Encoder.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.LOOPBACK_AUDIO_FILE}"
            )
        elif self.record_microphone and not self.record_loopback:
            Encoder.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.MICROPHONE_AUDIO_FILE}"
            )
        else:
            os.replace(
                src=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}", 
                dst=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}"
            )

        # Rename the final file and move it to output folder.
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        filename = f"{timestamp}.mp4"
        os.rename(
            src=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}", 
            dst=f"{Paths.RECORDINGS_DIR}/{filename}"
        )

    def __clean_up_temp_directory(self):
        """Removes all temporary files from the temp directory."""
        temp_file_names = []
        for attribute in dir(TempFiles):
            if not attribute.startswith('__'):
                temp_file_names.append(getattr(TempFiles, attribute))

        files_in_dir = os.listdir(Paths.TEMP_DIR)
        for file in files_in_dir:
            if file in temp_file_names:
                os.remove(os.path.join(Paths.TEMP_DIR, file))
