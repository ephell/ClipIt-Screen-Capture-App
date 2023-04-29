import multiprocessing as mp
import pyaudiowpatch as pyaudio
import time
import wave
from utils_audio import AudioUtils
from pydub import AudioSegment
import datetime
from math import ceil


class LoopbackRecorder(mp.Process, AudioUtils):
    """Records audio from the default loopback device."""

    loopback_device = None
    channels = None
    rate = None
    sample_size = None
    device_index = None

    def __init__(self, duration, barrier):
        super().__init__()
        self.duration = duration
        self.barrier = barrier

        loopback_device = self.get_default_loopback_device()
        if loopback_device is not None:
            self.loopback_device = loopback_device
            self.channels = loopback_device["maxInputChannels"]
            self.rate = int(loopback_device["defaultSampleRate"])
            self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
            self.device_index = loopback_device["index"]

    def record_loopback(self):
        with pyaudio.PyAudio() as p:
            output_file = wave.open("temp/TEMP-loopback.wav", 'wb')
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
                
                print("Waiting to pass barrier in loopback recording ... ")
                self.barrier.wait()
                print("Passed barrier in loopback recording process!")

                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S.%f")
                print("Started recording loopback: " + current_time)

                start_time = time.time()
                while time.time() - start_time < self.duration:
                    data = stream.read(
                        stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)
                    
            output_file.close()

    def run(self):
        print("Started loopback recording process ... ")
        started_playing = mp.Event()

        silence_player = _SilencePlayer(self.duration, started_playing)
        silence_player.start()

        # Wait for silence to start playing.
        started_playing.wait()

        self.record_loopback()

        silence_player.terminate()
        silence_player.join()
        print("Finished loopback recording process!")

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
        # Adding 5 to ensure that silence is played for long enough.
        self.duration = duration + 5
        self.started_playing = started_playing

    def run(self):
        silence = self.__generate_silence(self.duration)
        self.__play_silence(silence)

    def __generate_silence(self, duration):
        return {"data": b"\0\0" * int(44100 * duration),
                "sample_width": 2,
                "channels": 1,
                "frame_rate": 44100,
                "duration": duration}

    def __play_silence(self, silence):
        with pyaudio.PyAudio() as p:
            with p.open(
                format=p.get_format_from_width(silence["sample_width"]),
                channels=silence["channels"],
                rate=silence["frame_rate"],
                output=True
             ) as stream:
                started_playing_event_set = False
                for chunk in self.__make_chunks(silence):
                    stream.write(chunk)
                    if not started_playing_event_set:
                        self.started_playing.set()
                        started_playing_event_set = True
                        print("Silence start event set!")

    def __make_chunks(self, silence):
        """Break silence into chunks that are <chunk_length> ms long."""
        chunk_length = 500
        n_of_chunks = ceil(silence["duration"] * 1000 / float(chunk_length))
        chunk_size = int(len(silence["data"]) / n_of_chunks)
        return [silence["data"][i:i+chunk_size]
                for i in range(0, len(silence["data"]), chunk_size)]
    