import multiprocessing as mp
import pyaudiowpatch as pyaudio
import time
import wave
from utils_audio import AudioUtils
from pydub import AudioSegment
from pydub.playback import play


class LoopbackRecorder(mp.Process, AudioUtils):
    """Records audio from the default loopback device."""

    loopback_device = None
    channels = None
    rate = None
    sample_size = None
    device_index = None

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

        loopback_device = self.get_default_loopback_device()
        if loopback_device is not None:
            self.loopback_device = loopback_device
            self.channels = loopback_device["maxInputChannels"]
            self.rate = int(loopback_device["defaultSampleRate"])
            self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
            self.device_index = loopback_device["index"]

    def record_loopback(self):
        with pyaudio.PyAudio() as p:
            output_file = wave.open("AV-temp-audio.wav", 'wb')
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
        print("Started loopback recording process ... ")
        silence_player = _SilencePlayer(self.duration)
        silence_player.start()
        if silence_player.is_alive():
            self.record_loopback()
        silence_player.terminate()
        silence_player.join()
        print("Finished loopback recording process!")


class _SilencePlayer(mp.Process):
    """Plays silence in the background."""

    def __init__(self, duration):
        super().__init__()
        self.duration = duration + 5

    def run(self):
        print(f"Playing silence in the background ...")
        silence = AudioSegment.silent(
            duration=self.duration*1000,
            frame_rate=44100,
        )
        play(silence)
