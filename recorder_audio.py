from recorder_loopback import LoopbackRecorder
from recorder_microphone import MicrophoneRecorder
import multiprocessing as mp


class AudioRecorder:
    """Starts an appropriate recorder process."""

    def __init__(self, duration, loopback, microphone, barrier):
        self.duration = duration
        self.loopback = loopback
        self.microphone = microphone
        self.barrier = barrier

    def record(self):
        loopback_recorder = None
        microphone_recorder = None

        if self.loopback:
            loopback_recorder = LoopbackRecorder(self.duration, self.barrier)
            if loopback_recorder.loopback_device is not None:
                loopback_recorder.start()
            else:
                print("Can't record speaker audio! No loopback device found!")
        if self.microphone:
            microphone_recorder = MicrophoneRecorder(self.duration, self.barrier)
            if microphone_recorder.microphone is not None:
                microphone_recorder.start()
            else:
                print("Can't record input audio! No microphone found!")

        if loopback_recorder is not None and loopback_recorder.is_alive():
            loopback_recorder.join()
        if microphone_recorder is not None and microphone_recorder.is_alive():
            microphone_recorder.join()
