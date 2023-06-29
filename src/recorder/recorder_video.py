from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter, sleep

import cv2
import mss
import numpy as np

from settings import Paths, TempFiles


class VideoRecorder(mp.Process):
    """Records a video from a specified region/monitor."""

    def __init__(self, region, monitor, fps, barrier=None, stop_event=None):
        super().__init__()
        self.region = region
        self.monitor = monitor
        self.fps = fps
        self.barrier = barrier
        self.stop_event = stop_event

    def run(self):
        with mss.mss() as sct:
            monitor = {
                "left": int(self.region[0]),
                "top": int(self.region[1]),
                "width": int(self.region[2]),
                "height": int(self.region[3]),
                "mon": self.monitor,
            }

            if isinstance(self.barrier, mp.synchronize.Barrier):
                self.barrier.wait()
            else:
                log.warning(f"Barrier not set in: {self.__class__.__name__}. " \
                            "Final file might be out of sync.")

            log.info("Started recording video ... ")

            captured_frames = []
            frame_capture_times = []
            fps = self.fps
            start_time = perf_counter()
            while not self.stop_event.is_set():
                frame_start_time = perf_counter()
                screen = np.array(sct.grab(monitor))[:, :, :3]
                captured_frames.append(screen)
                frame_capture_time = perf_counter() - frame_start_time
                frame_capture_times.append(frame_capture_time)
                sleep_time = (1.0 / fps) - frame_capture_time
                if sleep_time > 0:
                    sleep(sleep_time)

        log.debug(
            f"Stopped capturing frames at: {perf_counter()}, " \
            f"Duration: {perf_counter() - start_time}"
        )
        log.debug("Writing frames to file ... ")

        fps = len(captured_frames) / (perf_counter() - start_time)
        out = cv2.VideoWriter(
            filename=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}",
            fourcc=cv2.VideoWriter_fourcc(*"mp4v"), 
            fps=fps,
            frameSize=(int(self.region[2]), int(self.region[3]))
        )
        for frame in captured_frames:
            out.write(frame)
        out.release()

        log.debug("Finished recording video!")
        log.debug("----------------------------------------")
        log.debug(f"Total frames captured: {len(captured_frames)}")
        log.debug(f"Average frame capture time: {np.mean(frame_capture_times)}")
        log.debug(f"Average FPS: {fps}")
        log.debug("----------------------------------------")
