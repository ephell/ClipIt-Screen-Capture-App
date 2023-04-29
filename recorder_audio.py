from recorder_loopback import LoopbackRecorder
from recorder_microphone import MicrophoneRecorder
import multiprocessing as mp


class AudioRecorder:
    """Starts an appropriate recorder process."""

    def __init__(self, duration, loopback_device, microphone, barrier):
        self.duration = duration
        self.loopback_device = loopback_device
        self.microphone = microphone
        self.barrier = barrier

    def record(self):
        if self.loopback_device:
            loopback_recorder = LoopbackRecorder(
                loopback_device=self.loopback_device,
                duration=self.duration, 
                barrier=self.barrier
            )
            loopback_recorder.start()
        else:
            print("Can't record speaker audio! No loopback device found!")

        if self.microphone:
            microphone_recorder = MicrophoneRecorder(
                microphone=self.microphone,
                duration=self.duration,
                barrier=self.barrier
            )
            microphone_recorder.start()
        else:
            print("Can't record input audio! No microphone found!")

        if self.loopback_device:
            loopback_recorder.join()
        if self.microphone:
            microphone_recorder.join()
