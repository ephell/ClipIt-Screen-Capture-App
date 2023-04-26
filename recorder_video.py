import numpy as np
import av
import multiprocessing as mp
import mss
import mss.tools
import time
from fractions import Fraction
import math

class VideoRecorder(mp.Process):

    def __init__(self, monitor, region, duration):
        super().__init__()
        self.monitor = monitor
        self.region = region
        self.duration = duration

    def run(self):
        print("Started video recording process ... ")

        container = av.open('AV-temp-video.mp4', mode='w')
        video_stream = container.add_stream('mpeg4')
        video_stream.width = self.region[2]
        video_stream.height = self.region[3]
        video_stream.bit_rate = 6000 * 1000
        video_stream.bit_rate_tolerance = 6000 * 1000

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

            print("Starting to capture frames ...")

            captured_frames = []
            frame_capture_times = []
            frame_count = 0
            start_time = time.time()
            fps = 30
            while time.time() - start_time <= self.duration:

                frame_capture_start_time = time.time()

                screen = np.array(sct.grab(monitor))
                screen = screen[..., :3]
                captured_frames.append(screen)

                frame_capture_end_time = time.time() - frame_capture_start_time
                frame_capture_times.append(frame_capture_end_time)
                frame_count += 1

                sleep_time = (1.0 / fps) - frame_capture_end_time
                if sleep_time > 0:
                    time.sleep(sleep_time)

            print("\n----------------------------------------")
            print("-------Finished capturing frames!-------")
            print("----------------------------------------")
            print("Total frames captured:", frame_count)
            print("Average frame capture time:", np.mean(frame_capture_times))
            print("Average FPS:", frame_count / self.duration)

            _fps = math.floor(frame_count / self.duration)
            video_stream.time_base = Fraction(_fps, 1)
            video_stream.rate = Fraction(_fps, 1)

            print("Video stream time base:", video_stream.time_base)
            print("Video stream rate:", video_stream.rate)
            print("----------------------------------------\n")

            print("Encoding frames ...")
            for frame in captured_frames:
                video_frame = av.VideoFrame.from_ndarray(frame, format='bgr24')
                packet = video_stream.encode(video_frame)
                if packet:
                    container.mux(packet)
            print("Finished encoding frames!")

        # Flushing the output and closing the container.
        packet = video_stream.encode(None)
        container.mux(packet)
        container.close()
        print("Encoded frames total:", video_stream.encoded_frame_count)
        print("Finished recording video!")
