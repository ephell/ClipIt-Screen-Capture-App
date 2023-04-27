import numpy as np
import multiprocessing as mp
import mss
import mss.tools
import time
from moviepy.editor import ImageSequenceClip

class VideoRecorder(mp.Process):

    def __init__(self, monitor, region, duration):
        super().__init__()
        self.monitor = monitor
        self.region = region
        self.duration = duration

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
            start_time = time.time()
            fps = 30
            while time.time() - start_time <= self.duration:

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

        _fps = captured_frame_count / self.duration

        clip = ImageSequenceClip(captured_frames, fps=_fps)
        clip.write_videofile("AV-temp-video.mp4", preset="ultrafast")

        print("Finished recording video!")
