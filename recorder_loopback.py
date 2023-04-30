from math import ceil
import multiprocessing as mp
import wave
from time import perf_counter

import pyaudiowpatch as pyaudio


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
        print("Started loopback recording process ... ")
        started_playing = mp.Event()
        silence_player = _SilencePlayer(self.duration, started_playing)
        silence_player.start()
        # Wait for silence to start playing.
        started_playing.wait()
        self.__record_loopback()
        silence_player.terminate()
        silence_player.join()
        print("Finished loopback recording process!")

    def __record_loopback(self):
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
                
                if isinstance(self.barrier, mp.synchronize.Barrier):
                    self.barrier.wait()
                else:
                    print(f"Barrier not set in: {self.__class__.__name__}. " \
                          "Final audio file might be out of sync.")

                start_time = perf_counter()
                while perf_counter() - start_time < self.duration:
                    data = stream.read(
                        stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)
                    
            output_file.close()


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

    def __make_chunks(self, silence):
        """Break silence into chunks that are <chunk_length> ms long."""
        chunk_length = 500
        n_of_chunks = ceil(silence["duration"] * 1000 / float(chunk_length))
        chunk_size = int(len(silence["data"]) / n_of_chunks)
        return [silence["data"][i:i+chunk_size]
                for i in range(0, len(silence["data"]), chunk_size)]
    