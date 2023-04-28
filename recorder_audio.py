from recorder_loopback import LoopbackRecorder
from recorder_microphone import MicrophoneRecorder

class AudioRecorder:
    
    def __init__(self, duration, loopback=True, microphone=True):
        self.duration = duration
        self.loopback = loopback
        self.microphone = microphone

    def record(self):
        if self.loopback:
            loopback_recorder = LoopbackRecorder(self.duration)
            loopback_recorder.start()
        if self.microphone:
            microphone_recorder = MicrophoneRecorder(self.duration)
            microphone_recorder.start()
