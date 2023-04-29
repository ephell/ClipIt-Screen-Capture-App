import numpy as np
import multiprocessing as mp
import mss
import mss.tools
import time
from moviepy.editor import ImageSequenceClip
import datetime


class VideoRecorder(mp.Process):
    """Records a video from a specified region/monitor."""

    def __init__(self, monitor, region, duration, fps, barrier):
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
            captured_frame_count = 0
            fps = self.fps

            print("Waiting to pass barrier in video capture ... ")
            self.barrier.wait()
            print("Passed barrier in video capture process!")

            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S.%f")
            print("Started capturing video: " + current_time)

            
            start_time = time.time()
            while time.time() - start_time < self.duration:

                frame_capture_start_time = time.time()

                screen = np.array(sct.grab(monitor))
                screen = np.flip(screen[..., :3], axis=-1)
                captured_frames.append(screen)
                captured_frame_count += 1
                
                frame_capture_end_time = time.time() - frame_capture_start_time
                frame_capture_times.append(frame_capture_end_time)

                sleep_time = (1.0 / fps) - frame_capture_end_time
                if sleep_time > 0:
                    time.sleep(sleep_time)

        print("\n----------------------------------------")
        print("Total frames captured:", captured_frame_count)
        print("Average frame capture time:", np.mean(frame_capture_times))
        print("Average FPS:", captured_frame_count / self.duration)
        print("----------------------------------------\n")

        print("Writing captured frames to video file ... ")
        precise_fps = captured_frame_count / self.duration
        clip = ImageSequenceClip(captured_frames, fps=precise_fps)
        clip.write_videofile(
            filename="temp/TEMP-video.mp4",
            preset="ultrafast",
            logger=None
        )
        print("Finished writing frames!")

        print("Finished video recording process!")
