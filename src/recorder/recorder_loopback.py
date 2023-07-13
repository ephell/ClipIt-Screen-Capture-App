from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
import threading
from time import perf_counter
import wave

import pyaudiowpatch as pyaudio

from settings.settings import Settings


class LoopbackRecorder(mp.Process):
    """Records audio from the default loopback device."""

    def __init__(
            self, 
            loopback_device: dict, # AudioUtils.get_default_loopback_device() 
            barrier: mp.Barrier=None, 
            stop_event: mp.Event=None
        ):
        super().__init__()
        self.barrier = barrier
        self.stop_event = stop_event
        self.channels = loopback_device["maxInputChannels"]
        self.sample_rate = int(loopback_device["defaultSampleRate"])
        self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
        self.device_index = loopback_device["index"]

    def run(self):
        is_silence_playing = mp.Event()
        is_recording_finished = threading.Event()
        silence_player = _SilencePlayer(
            is_silence_playing=is_silence_playing, 
            is_recording_finished=is_recording_finished
        )
        silence_player.start()
        is_silence_playing.wait()
        self.__record_loopback(is_recording_finished)
        silence_player.join()
        
    def __record_loopback(self, is_recording_finished):
        with pyaudio.PyAudio() as p:
            output_file = wave.open(
                f=Settings.get_temp_file_paths().LOOPBACK_AUDIO_FILE,
                mode="wb"
            )
            output_file.setnchannels(self.channels)
            output_file.setframerate(self.sample_rate)
            output_file.setsampwidth(self.sample_size)

            with p.open(
                format=pyaudio.paInt16,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                input_device_index=self.device_index,
            ) as stream:
                # Syncing with other recording processes.
                if isinstance(self.barrier, mp.synchronize.Barrier):
                    self.barrier.wait()
                else:
                    log.warning(
                        f"Barrier not set in: {self.__class__.__name__}. " \
                        "Final file might be out of sync."
                    )

                log.info("Started recording loopback audio ... ")
                start_time = perf_counter()
                while not self.stop_event.is_set():
                    data = stream.read(
                        num_frames=stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)

            log.debug(
                f"Stopped recording loopback audio at: {perf_counter()}, " \
                f"Duration: {perf_counter() - start_time}"
            )

            output_file.close()
            # Letting the silence player thread know that it can stop.
            is_recording_finished.set()
            log.info("Finished recording loopback audio!")


class _SilencePlayer(threading.Thread):
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

    def __init__(self, is_silence_playing, is_recording_finished):
        super().__init__()
        self.daemon = True
        self.is_silence_playing = is_silence_playing
        self.is_recording_finished = is_recording_finished
        self.sample_rate = 44100
        self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16)
        self.channels = 1

    def run(self):
        self.__play()

    def __play(self):
        with pyaudio.PyAudio() as p:
            with p.open(
                format=p.get_format_from_width(self.sample_size),
                channels=self.channels,
                rate=self.sample_rate,
                output=True
             ) as stream:
                is_silence_playing_event_set = False
                while not self.is_recording_finished.is_set():
                    for _ in range(int(self.sample_rate)):
                        sample = self.__generate_silent_sample(
                            size=self.sample_size,
                            channels=self.channels,
                        )
                        stream.write(sample)
                        if not is_silence_playing_event_set:
                            self.is_silence_playing.set()
                            is_silence_playing_event_set = True

    def __generate_silent_sample(self, size, channels):
        return b"\0" * size * channels
