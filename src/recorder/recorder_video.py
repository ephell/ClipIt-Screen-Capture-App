from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter, sleep

import imageio
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
        self.macro_block_size = 2
        self.quality = 5 # 10 is max (pretty large file size)

    def run(self):
        fps, total_frames_captured = self.__capture_and_save_video()
        if self.file_generation_choice_event is not None:
            self.file_generation_choice_event.wait()
        if (
            self.file_generation_choice_value is None
            or self.file_generation_choice_value.value == True
        ):
            self.__reencode_with_precise_fps(fps, total_frames_captured)

    def __capture_and_save_video(self):
        with mss.mss() as sct:
            monitor = {
                "left": int(self.region[0]),
                "top": int(self.region[1]),
                "width": int(self.region[2]),
                "height": int(self.region[3]),
                "mon": self.monitor,
            }

            frame_writer = imageio.get_writer(
                self.captured_filename,
                fps=self.fps,
                quality=self.quality,
                macro_block_size=self.macro_block_size
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

            total_frames_captured = 0
            while not self.stop_event.is_set():
                frame_start_time = perf_counter()
                frame = np.array(sct.grab(monitor))
                frame = self.__remove_alpha_channel(frame)
                frame = self.__flip_from_BGRA_to_RGB(frame)
                total_frames_captured += 1
                frame_writer.append_data(frame)
                frame_capture_time = perf_counter() - frame_start_time
                sleep_time = (1.0 / self.fps) - frame_capture_time
                if sleep_time > 0:
                    sleep(sleep_time)

            frame_writer.close()
            log.info("Finished recording video!")

        avg_fps = total_frames_captured / (perf_counter() - start_time)

        return avg_fps, total_frames_captured

    def __remove_alpha_channel(self, frame: np.ndarray):
        return frame[:, :, :3]

    def __flip_from_BGRA_to_RGB(self, frame: np.ndarray):
        return np.flip(frame[:, :, :3], 2)

    def __reencode_with_precise_fps(self, fps, total_frames_in_input_file):
        """Rewrites the video file with precise fps."""
        log.info("Started reencoding video ... ")
        input_video_reader = imageio.get_reader(self.captured_filename)
        output_video_writer = imageio.get_writer(
            self.reencoded_filename,
            fps=fps,
            quality=self.quality,
            macro_block_size=self.macro_block_size
        )
        frames_written = 0
        for frame in input_video_reader:
            output_video_writer.append_data(frame)
            frames_written += 1
            if self.reencoding_progress_queue is not None:
                progress = (frames_written / total_frames_in_input_file) * 100
                self.reencoding_progress_queue.put(progress)
        input_video_reader.close()
        output_video_writer.close()
        log.info("Finished reencoding video!")
