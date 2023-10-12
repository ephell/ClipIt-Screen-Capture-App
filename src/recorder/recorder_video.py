from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter, sleep

import cv2
import mss
import numpy as np

from settings.settings import Settings


class VideoRecorder(mp.Process):
    """Continuously captures specified region and saves to a video file."""

    def __init__(
            self, 
            region: list[int, int, int, int],
            monitor: int,
            fps: int,
            barrier: mp.Barrier=None,
            stop_event: mp.Event=None,
            reencoding_progress_queue: mp.Queue=None, # Mp.Manager().Queue() is faster
            recording_started: mp.Value=None, # Float value set to -1.0
            file_generation_choice_event: mp.Event=None,
            file_generation_choice_value: mp.Value=None
        ):
        super().__init__()
        self.region = region
        self.monitor = monitor
        self.fps = fps
        self.barrier = barrier
        self.stop_event = stop_event
        self.reencoding_progress_queue = reencoding_progress_queue
        self.recording_started = recording_started
        self.file_generation_choice_event = file_generation_choice_event
        self.file_generation_choice_value = file_generation_choice_value
        self.captured_filename = Settings.get_temp_file_paths().CAPTURED_VIDEO_FILE
        self.reencoded_filename = Settings.get_temp_file_paths().REENCODED_VIDEO_FILE
        self.frame_size = (int(self.region[2]), int(self.region[3]))
        self.cv2_writer_fourcc = "mp4v"

    def run(self):
        fps, total_frames_captured = self.__capture_and_save_video()
        if self.file_generation_choice_event is not None:
            self.file_generation_choice_event.wait()
        if (
            self.file_generation_choice_value is None
            or self.file_generation_choice_value.value == True
        ):
            self.__reencode_captured_video(fps, total_frames_captured)

    def __capture_and_save_video(self):
        with mss.mss() as sct:
            monitor = {
                "left": int(self.region[0]),
                "top": int(self.region[1]),
                "width": int(self.region[2]),
                "height": int(self.region[3]),
                "mon": self.monitor,
            }
            encoder = cv2.VideoWriter(
                filename=self.captured_filename,
                fourcc=cv2.VideoWriter_fourcc(*self.cv2_writer_fourcc), 
                fps=self.fps,
                frameSize=self.frame_size
            )

            # Syncing with other recording processes.
            if isinstance(self.barrier, mp.synchronize.Barrier):
                self.barrier.wait()
            else:
                log.warning(
                    f"Barrier not set in: {self.__class__.__name__}. " \
                    "Final file might be out of sync."
                )

            log.info("Started recording video ... ")
            # Letting the main thread know that recording has started.
            start_time = perf_counter()
            if self.recording_started is not None:
                self.recording_started.value = start_time

            fps = self.fps
            total_frames_captured = 0
            while not self.stop_event.is_set():
                frame_start_time = perf_counter()
                screen = np.array(sct.grab(monitor))[:, :, :3]
                total_frames_captured += 1
                encoder.write(screen)
                frame_capture_time = perf_counter() - frame_start_time
                sleep_time = (1.0 / fps) - frame_capture_time
                if sleep_time > 0:
                    sleep(sleep_time)
            encoder.release()
            log.info("Finished recording video!")

        avg_fps = total_frames_captured / (perf_counter() - start_time)

        return avg_fps, total_frames_captured

    def __reencode_captured_video(self, fps, total_frames_in_input_file):
        """Reencodes video with precise fps."""
        video_to_reencode = cv2.VideoCapture(self.captured_filename)
        reencoder = cv2.VideoWriter(
            filename=self.reencoded_filename,
            fourcc=cv2.VideoWriter_fourcc(*self.cv2_writer_fourcc), 
            fps=fps,
            frameSize=self.frame_size
        )
        log.info("Started reencoding video ... ")
        frames_reencoded = 0
        while video_to_reencode.isOpened():
            frame_read_successfully, frame = video_to_reencode.read()
            if frame_read_successfully:
                reencoder.write(frame)
                frames_reencoded += 1
                if self.reencoding_progress_queue is not None:
                    progress = (frames_reencoded / total_frames_in_input_file) * 100
                    self.reencoding_progress_queue.put(progress)
            else:
                break
        video_to_reencode.release()
        reencoder.release()
        log.info("Finished reencoding video!")
