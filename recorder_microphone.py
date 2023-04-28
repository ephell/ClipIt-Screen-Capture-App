import multiprocessing as mp
import pyaudiowpatch as pyaudio
import time
import wave
from utils_audio import AudioUtils

class MicrophoneRecorder(mp.Process, AudioUtils):
    
    microphone = None
    channels = None
    rate = None
    sample_size = None
    device_index = None

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

        microphone = self.get_default_microphone()
        if microphone is not None:
            self.microphone = microphone
            self.channels = microphone["maxInputChannels"]
            self.rate = int(microphone["defaultSampleRate"])
            self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
            self.device_index = microphone["index"]

    def record_microphone(self):
        with pyaudio.PyAudio() as p:
            output_file = wave.open("AV-temp-mic-audio.wav", 'wb')
            output_file.setnchannels(self.channels)
            output_file.setframerate(self.rate)
            output_file.setsampwidth(self.sample_size)

            with p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                frames_per_buffer=self.sample_size,
                input=True,
                input_device_index=self.device_index,
            ) as stream:
                start_time = time.time()
                while time.time() - start_time <= self.duration:
                    data = stream.read(
                        stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)

            output_file.close()

    def run(self):
        print("Started microphone recording process ... ")
        self.record_microphone()
        print("Finished microphone recording process!")