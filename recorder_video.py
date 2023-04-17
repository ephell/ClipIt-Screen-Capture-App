import numpy as np
import av
import multiprocessing as mp
import mss
import mss.tools
import time
from fractions import Fraction
import math

class VideoRecorder(mp.Process):

    def __init__(self, monitor, region, duration, fps):
        super().__init__()
        self.monitor = monitor
        self.region = region
        self.duration = duration
        self.fps = fps

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

            start_time = time.time()
            base_time = 0
            is_base_time_set = False

            while time.time() - start_time <= self.duration:

                screen = np.array(sct.grab(monitor))
                screen = screen[..., :3]
                frame = av.VideoFrame.from_ndarray(screen, format='bgr24')

                if not is_base_time_set:
                    is_base_time_set = True
                    base_time = time.time() - start_time
                    predicted_frame_count = math.floor(1 / base_time)
                    print("Predicted frame count: ", predicted_frame_count)
                    video_stream.time_base = Fraction(1, predicted_frame_count)
                    video_stream.rate = Fraction(predicted_frame_count / 1)

                packet = video_stream.encode(frame)
                if packet:
                    container.mux(packet)

        container.close()
        print("Encoded frame total: " + video_stream.encoded_frame_count)
        print("Finished recording video!")
