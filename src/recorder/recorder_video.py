from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter, sleep

import cv2
import mss
import numpy as np

from settings import Paths, TempFiles


class VideoRecorder(mp.Process):
    """Continuously captures specified region and saves to a video file."""

    def __init__(
            self, 
            region, 
            monitor, 
            fps, 
            barrier=None,
            stop_event=None,
            reencoding_progress_queue=None
        ):
        super().__init__()
        self.region = region
        self.monitor = monitor
        self.fps = fps
        self.barrier = barrier
        self.stop_event = stop_event
        self.reencoding_progress_queue = reencoding_progress_queue
        self.captured_filename = f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}"
        self.reencoded_filename = f"{Paths.TEMP_DIR}/{TempFiles.REENCODED_VIDEO_FILE}"
        self.frame_size = (int(self.region[2]), int(self.region[3]))
        self.cv2_writer_fourcc = "mp4v"

    def run(self):
        fps, total_frames_captured = self.__capture_and_save_video()
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

            if isinstance(self.barrier, mp.synchronize.Barrier):
                self.barrier.wait()
            else:
                log.warning(
                    f"Barrier not set in: {self.__class__.__name__}. " \
                    "Final file might be out of sync."
                )

            log.info("Started recording video ... ")
            fps = self.fps
            total_frames_captured = 0
            start_time = perf_counter()
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
