from math import ceil
import multiprocessing as mp
import wave
from time import perf_counter

import pyaudiowpatch as pyaudio

from settings import Paths, TempFiles


class LoopbackRecorder(mp.Process):
    """Records audio from the default loopback device."""

    def __init__(self, loopback_device, duration, barrier=None):
        super().__init__()
        self.duration = duration
        self.barrier = barrier
        self.channels = loopback_device["maxInputChannels"]
        self.rate = int(loopback_device["defaultSampleRate"])
        self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
        self.device_index = loopback_device["index"]

    def run(self):
        started_playing = mp.Event()
        silence_player = _SilencePlayer(self.duration, started_playing)
        silence_player.start()
        # Wait for silence to start playing.
        started_playing.wait()
        self.__record_loopback()
        silence_player.terminate()
        silence_player.join()

    def __record_loopback(self):
        with pyaudio.PyAudio() as p:
            output_file = wave.open(
                f=f"{Paths.TEMP_DIR}/{TempFiles.LOOPBACK_AUDIO_FILE}",
                mode="wb"
            )
            output_file.setnchannels(self.channels)
            output_file.setframerate(self.rate)
            output_file.setsampwidth(self.sample_size)

            with p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.rate,
                input=True,
                input_device_index=self.device_index,
            ) as stream:
                
                if isinstance(self.barrier, mp.synchronize.Barrier):
                    self.barrier.wait()
                else:
                    print(f"Barrier not set in: {self.__class__.__name__}. " \
                          "Final audio file might be out of sync.")

                print("Started recording loopback audio ... ")

                start_time = perf_counter()
                while perf_counter() - start_time < self.duration:
                    data = stream.read(
                        num_frames=stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)
                    
            output_file.close()

            print("Finished recording loopback audio!")


class _SilencePlayer(mp.Process):
    """
    Plays silence in the background. 
    
    WASAPI loopback recording requires some kind of data to be coming in 
    for it to start capturing. If silence is not played then only parts 
    of audio that are actually heard by the user would be recorded. In 
    most cases this would generate an audio file that is shorter than 
    the duration specified, because the user might not be playing audio
    for the whole duration. This would also make it very hard to 
    properly sync the audio with the video.

    """

    def __init__(self, duration, started_playing):
        super().__init__()
        self.duration = duration
        self.started_playing = started_playing
        self.sample_rate = 44100
        self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16)
        self.channels = 1

    def run(self):
        self.__play_silence()

    def __play_silence(self):
        with pyaudio.PyAudio() as p:
            with p.open(
                format=p.get_format_from_width(self.sample_size),
                channels=self.channels,
                rate=self.sample_rate,
                output=True
             ) as stream:
                started_playing_event_set = False
                for _ in range(int(self.sample_rate * self.duration)):
                    sample = self.__generate_silent_sample(
                        size=self.sample_size,
                        channels=self.channels,
                    )
                    stream.write(sample)
                    if not started_playing_event_set:
                        self.started_playing.set()
                        started_playing_event_set = True

    def __generate_silent_sample(self, size, channels):
        return b"\0" * size * channels
