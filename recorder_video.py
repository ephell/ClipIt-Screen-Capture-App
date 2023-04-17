import numpy as np
import av
import multiprocessing as mp
from PIL import ImageGrab

class VideoRecorder(mp.Process):

    def __init__(self, record_duration):
        super().__init__()
        self.record_duration = record_duration

    def run(self):
        print("Started video recording process ... ")

        container = av.open('AV-temp-video.mp4', mode='w')
        video_stream = container.add_stream('libx264', rate=30)
        video_stream.width = 1920
        video_stream.height = 1080

        fps = 30
        duration = self.record_duration
        num_frames = fps * duration

        for _ in range(num_frames):
            screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            frame = av.VideoFrame.from_ndarray(screen, format='rgb24')
            packet = video_stream.encode(frame)
            if packet:
                container.mux(packet)

        video_stream.encode(None)
        container.close()

        print("Finished recording video!")