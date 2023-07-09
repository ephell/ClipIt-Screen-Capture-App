from logger import GlobalLogger
log = GlobalLogger.LOGGER

import datetime
import multiprocessing as mp
import os
import threading

from proglog import ProgressBarLogger
from PySide6.QtCore import Signal, QObject

from utilities.video import VideoUtils
from recorder.recorder_loopback import LoopbackRecorder
from recorder.recorder_microphone import MicrophoneRecorder
from recorder.recorder_video import VideoRecorder
from settings import Paths, TempFiles
from utilities.audio import AudioUtils


class Recorder(QObject, threading.Thread):
    """Recording controller."""

    # Emits number of steps the final file generation progress bar should have.
    recorder_stop_event_set_signal = Signal(int)
    video_reencoding_progress_signal = Signal(int)
    video_and_audio_merging_progress_signal = Signal(int)
    audio_merging_progress_signal = Signal(int)
    # Emits the path to the final video file.
    file_generation_finished_signal = Signal(str)

    show_dialog = Signal()

    def __init__(
            self,
            record_video,
            record_loopback,
            record_microphone,
            region,
            monitor,
            fps,
            stop_event
        ):
        super().__init__()
        self.record_video = record_video
        self.record_loopback = record_loopback
        self.record_microphone = record_microphone
        self.region = region
        self.monitor = monitor
        self.fps = fps
        self.stop_event = stop_event
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
        self.__clean_up_temp_directory()

        for recorder in self.__get_recorders():
            recorder.start()

        self.stop_event.wait()

        for recorder in self.__get_recorders():
            recorder.stop_event.set()

        self.recorder_stop_event_set_signal.emit(len(self.__get_recorders()))
        self.__transmit_video_reencoding_progress()
        final_video_path = self.__generate_final_video()
        self.file_generation_finished_signal.emit(final_video_path)

        for recorder in self.__get_recorders():
            recorder.join()

        self.__clean_up_temp_directory()


    def __initialize_video_recorder(self):
        self.video_recorder_stop_event = mp.Event()
        self.video_recorder = VideoRecorder(
            region=self.region,
            monitor=self.monitor,
            fps=self.fps,
            stop_event=self.video_recorder_stop_event,
            reencoding_progress_queue=mp.Manager().Queue()
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

    def __transmit_video_reencoding_progress(self):
        while True:
            if not self.video_recorder.is_alive():
                break
            elif not self.video_recorder.reencoding_progress_queue.empty():
                self.video_reencoding_progress_signal.emit(
                    self.video_recorder.reencoding_progress_queue.get()
                )

    def __generate_final_video(self):
        """Generates the final file from recorded temporary files."""
        # Create loggers
        video_and_audio_merging_logger = _MergingProgressLogger(
            progress_signal=self.video_and_audio_merging_progress_signal
        )
        if len(self.__get_recorders()) == 3:
            audio_merging_logger = _MergingProgressLogger(
                progress_signal=self.audio_merging_progress_signal
            )

        # Merge video/audio as needed
        if self.record_loopback and self.record_microphone:
            VideoUtils.merge_audio(
                first_clip_path=f"{Paths.TEMP_DIR}/{TempFiles.LOOPBACK_AUDIO_FILE}", 
                second_clip_path=f"{Paths.TEMP_DIR}/{TempFiles.MICROPHONE_AUDIO_FILE}",
                output_path=f"{Paths.TEMP_DIR}/{TempFiles.MERGED_AUDIO_FILE}",
                logger=audio_merging_logger
            )
            VideoUtils.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.REENCODED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.MERGED_AUDIO_FILE}",
                output_path=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}",
                logger=video_and_audio_merging_logger
            )
        elif self.record_loopback and not self.record_microphone:
            VideoUtils.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.REENCODED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.LOOPBACK_AUDIO_FILE}",
                output_path=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}",
                logger=video_and_audio_merging_logger
            )
        elif self.record_microphone and not self.record_loopback:
            VideoUtils.merge_video_with_audio(
                video_path=f"{Paths.TEMP_DIR}/{TempFiles.REENCODED_VIDEO_FILE}",
                audio_path=f"{Paths.TEMP_DIR}/{TempFiles.MICROPHONE_AUDIO_FILE}",
                output_path=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}",
                logger=video_and_audio_merging_logger
            )
        else:
            os.replace(
                src=f"{Paths.TEMP_DIR}/{TempFiles.REENCODED_VIDEO_FILE}", 
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

        final_file_path = os.path.join(Paths.RECORDINGS_DIR, filename)
        final_file_path = final_file_path.replace('\\', '/')

        return final_file_path

    def __clean_up_temp_directory(self):
        """Removes all temporary files from the temp directory."""
        temp_filenames = []
        for attribute in dir(TempFiles):
            if not attribute.startswith('__'):
                temp_filenames.append(getattr(TempFiles, attribute))

        files_in_dir = os.listdir(Paths.TEMP_DIR)
        for file in files_in_dir:
            if file in temp_filenames:
                os.remove(os.path.join(Paths.TEMP_DIR, file))


class _MergingProgressLogger(ProgressBarLogger):

    def __init__(self, progress_signal):
        super().__init__()
        self.progress_signal = progress_signal

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "index":
            percentage = (value / self.bars[bar]["total"]) * 100
            self.progress_signal.emit(percentage)
