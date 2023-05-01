from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter, sleep

from moviepy.editor import ImageSequenceClip
import mss
import numpy as np

from settings import Paths, TempFiles


class VideoRecorder(mp.Process):
    """Records a video from a specified region/monitor."""

    def __init__(self, monitor, region, duration, fps, barrier=None):
        super().__init__()
        self.monitor = monitor
        self.region = region
        self.duration = duration
        self.fps = fps
        self.barrier = barrier

    def run(self):
        with mss.mss() as sct:
            if self.monitor == 2:
                self.region[0] += sct.monitors[self.monitor]["left"]

            monitor = {
                "left": self.region[0],
                "top": self.region[1],
                "width": self.region[2],
                "height": self.region[3],
                "mon": self.monitor,
            }

            captured_frames = []
            frame_capture_times = []
            fps = self.fps

            if isinstance(self.barrier, mp.synchronize.Barrier):
                self.barrier.wait()
            else:
                log.warning(f"Barrier not set in: {self.__class__.__name__}. " \
                            "Final audio file might be out of sync.")

            log.info("Started recording video ... ")

            start_time = perf_counter()
            while perf_counter() - start_time < self.duration:

                frame_start_time = perf_counter()

                screen = np.array(sct.grab(monitor))
                screen = np.flip(screen[..., :3], axis=-1)
                captured_frames.append(screen)
                
                frame_end_time = perf_counter() - frame_start_time
                frame_capture_times.append(frame_end_time)

                sleep_time = (1.0 / fps) - frame_end_time
                if sleep_time > 0:
                    sleep(sleep_time)

        precise_fps = len(captured_frames) / self.duration
        clip = ImageSequenceClip(captured_frames, fps=precise_fps)
        clip.write_videofile(
            filename=f"{Paths.TEMP_DIR}/{TempFiles.CAPTURED_VIDEO_FILE}",
            preset="ultrafast",
            logger=None
        )

        log.info("Finished recording video!")
        log.info("----------------------------------------")
        log.info(f"Total frames captured: {len(captured_frames)}")
        log.info(f"Average frame capture time: {np.mean(frame_capture_times)}")
        log.info(f"Average FPS: {precise_fps}")
        log.info("----------------------------------------")
