import datetime
import multiprocessing as mp
import os
import threading
import queue

from proglog import ProgressBarLogger
from PySide6.QtCore import Signal, QObject

from src.recorder.recorder_loopback import LoopbackRecorder
from src.recorder.recorder_video import VideoRecorder
from src.settings.settings import Settings
from src.utilities.video import VideoUtils
from src.utilities.audio import AudioUtils


class Recorder(QObject, threading.Thread):
    """Recording controller."""

    # Emits start time of the recording process.
    recording_started_signal = Signal(float)
    # Emits a signal to notify that recording has stopped.
    recorder_stop_event_set_signal = Signal()
    # Emits number of steps the final file generation progress bar should have.
    file_generation_started_signal = Signal(int)
    # Final file generation progress signals.
    video_reencoding_progress_signal = Signal(int)
    video_and_audio_merging_progress_signal = Signal(int)
    # Emits the path to the final video file.
    file_generation_finished_signal = Signal(str)

    def __init__(
            self,
            record_video: bool,
            record_loopback: bool,
            region: list[int, int, int, int],
            monitor: int,
            stop_event: threading.Event,
            file_generation_choice_event: threading.Event=None,
            generate_final_file=True,
        ):
        super().__init__()
        self.setName("Recorder")
        self.record_video = record_video
        self.record_loopback = record_loopback
        self.region = region
        self.monitor = monitor
        self.stop_event = stop_event
        self.file_generation_choice_event = file_generation_choice_event
        self.generate_final_file = generate_final_file
        self.recording_started = mp.Value("d", -1.0)
        self.video_recorder = None
        self.video_recorder_stop_event = None
        self.video_recorder_file_generation_choice_event = None
        self.video_recorder_file_generation_choice_value = None
        self.loopback_recorder = None
        self.loopback_recorder_stop_event = None
    
        if self.record_video:
            self.__initialize_video_recorder()
        if self.record_loopback:
            self.__initialize_loopback_recorder()

        # Make sure all recorders start at the same time.
        barrier = mp.Barrier(len(self.__get_recorders()))
        for recorder in self.__get_recorders():
            recorder.barrier = barrier

    def run(self):
        self.recording_started_checker = _RecordingStartedChecker(
            self.recording_started,
            self.recording_started_signal
        )
        self.recording_started_checker.start()

        for recorder in self.__get_recorders():
            recorder.start()

        self.stop_event.wait()

        for recorder in self.__get_recorders():
            recorder.stop_event.set()

        self.recorder_stop_event_set_signal.emit()

        # Wait for users' choice
        if self.file_generation_choice_event is not None:
            self.file_generation_choice_event.wait()

        # Final file generation based on users' choice
        if self.video_recorder_file_generation_choice_event:
            if self.generate_final_file:
                self.video_recorder_file_generation_choice_value.value = True
            else:
                self.video_recorder_file_generation_choice_value.value = False
            self.video_recorder_file_generation_choice_event.set()

        if self.generate_final_file:
            self.file_generation_started_signal.emit(len(self.__get_recorders()))
            self.__transmit_video_reencoding_progress()
            final_video_path = self.__generate_final_video()
            self.file_generation_finished_signal.emit(final_video_path)

        for recorder in self.__get_recorders():
            recorder.join()

        self.__clean_up_temp_directory()

    def __initialize_video_recorder(self):
        self.video_recorder_stop_event = mp.Event()
        self.video_recorder_file_generation_choice_event = mp.Event()
        self.video_recorder_file_generation_choice_value = mp.Value("b", True)
        self.video_reencoding_progress_queue = mp.Queue()
        self.video_recorder = VideoRecorder(
            region=self.region,
            monitor=self.monitor,
            stop_event=self.video_recorder_stop_event,
            file_generation_choice_event=self.video_recorder_file_generation_choice_event,
            file_generation_choice_value=self.video_recorder_file_generation_choice_value,
            reencoding_progress_queue=self.video_reencoding_progress_queue,
            recording_started=self.recording_started,
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

    def __get_recorders(self):
        recorders = [
            self.video_recorder, 
            self.loopback_recorder
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
        # Merge video with audio into a final file.
        logger = _MergingProgressLogger(self.video_and_audio_merging_progress_signal)
        temp_file_paths = Settings.get_temp_file_paths()
        VideoUtils.merge_video_with_audio(
            video_path=temp_file_paths.REENCODED_VIDEO_FILE,
            audio_path=temp_file_paths.LOOPBACK_AUDIO_FILE,
            output_path=temp_file_paths.FINAL_FILE,
            logger=logger
        )
        # Rename the final file and move it to output folder.
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        old_file_path = temp_file_paths.FINAL_FILE
        new_file_path = f"{Settings.get_capture_dir_path()}/{timestamp}.mp4"
        os.rename(
            src=old_file_path,
            dst=new_file_path
        )
        # Replace backslashes with forward slashes so that there are no
        # errors when opening the file in the editor after generating it.
        new_file_path = new_file_path.replace('\\', '/')
        return new_file_path

    def __clean_up_temp_directory(self):
        """Removes all temporary files from the temp directory."""
        for attribute in dir(Settings.get_temp_file_paths()):
            if not attribute.startswith('__'):
                path = getattr(Settings.get_temp_file_paths(), attribute)
                if not os.path.isdir(path):
                    if os.path.exists(path):
                        try:
                            os.remove(path)
                        except PermissionError:
                            print(
                                f"PermissionError when trying to delete: {path} | "
                                f"File is probably in use by another process."
                            )


class _RecordingStartedChecker(threading.Thread):
    """Checks whether recording in 'VideoRecorder' has started."""

    def __init__(self, recording_started, recording_started_signal):
        super().__init__()
        self.recording_started = recording_started
        self.recording_started_signal = recording_started_signal

    def run(self):
        while True:
            if self.recording_started.value >= 0:
                self.recording_started_signal.emit(self.recording_started.value)
                break


class _MergingProgressLogger(ProgressBarLogger):

    def __init__(self, progress_signal):
        super().__init__()
        self.progress_signal = progress_signal

    def bars_callback(self, bar, attr, value, old_value=None):
        if attr == "index":
            percentage = (value / self.bars[bar]["total"]) * 100
            self.progress_signal.emit(percentage)
