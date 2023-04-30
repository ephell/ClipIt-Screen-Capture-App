import multiprocessing as mp
from time import perf_counter, sleep

from moviepy.editor import ImageSequenceClip
import mss
import numpy as np


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
        print("Started video recording process ... ")

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
                print(f"Barrier not set in: {self.__class__.__name__}. " \
                        "Final audio file might be out of sync.")

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

        print("\n----------------------------------------")
        print("Total frames captured:", len(captured_frames))
        print("Average frame capture time:", np.mean(frame_capture_times))
        print("Average FPS:", len(captured_frames) / self.duration)
        print("----------------------------------------\n")

        print("Writing captured frames to video file ... ")
        precise_fps = len(captured_frames) / self.duration
        clip = ImageSequenceClip(captured_frames, fps=precise_fps)
        clip.write_videofile(
            filename="temp/TEMP-video.mp4",
            preset="ultrafast",
            logger=None
        )
        print("Finished writing frames!")

        print("Finished video recording process!")