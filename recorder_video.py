import numpy as np
import av
import multiprocessing as mp
import mss
import mss.tools


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
        video_stream = container.add_stream('libx264', rate=30)
        video_stream.width = 1920
        video_stream.height = 1080

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

            total_frames = self.fps * self.duration
            for _ in range(total_frames):
                screen = np.array(sct.grab(monitor))
                screen = screen[..., :3]
                frame = av.VideoFrame.from_ndarray(screen, format='bgr24')
                packet = video_stream.encode(frame)
                if packet:
                    container.mux(packet)

        video_stream.encode(None)
        container.close()

        print("Finished recording video!")
