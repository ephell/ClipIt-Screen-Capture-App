from logger import GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter
import wave

import pyaudiowpatch as pyaudio

from settings import Paths, TempFiles


class MicrophoneRecorder(mp.Process):
    """Records audio from the default microphone."""

    def __init__(
            self, 
            microphone: dict, # AudioUtils.get_default_microphone() 
            barrier: mp.Barrier=None,
            stop_event: mp.Event=None
        ):
        super().__init__()
        self.barrier = barrier
        self.stop_event = stop_event
        self.channels = microphone["maxInputChannels"]
        self.rate = int(microphone["defaultSampleRate"])
        self.sample_size = pyaudio.get_sample_size(pyaudio.paInt16) 
        self.device_index = microphone["index"]

    def run(self):
        self.__record_microphone()

    def __record_microphone(self):
        with pyaudio.PyAudio() as p:
            output_file = wave.open(
                f=f"{Paths.TEMP_DIR}/{TempFiles.MICROPHONE_AUDIO_FILE}",
                mode="wb"
            )
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
                # Syncing with other recording processes.
                if isinstance(self.barrier, mp.synchronize.Barrier):
                    self.barrier.wait()
                else:
                    log.warning(
                        f"Barrier not set in: {self.__class__.__name__}. " \
                        "Final file might be out of sync."
                    )

                log.info("Started recording microphone audio ... ")
                start_time = perf_counter()
                while not self.stop_event.is_set():
                    data = stream.read(
                        num_frames=stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)

            log.debug(
                f"Stopped recording microphone audio at: {perf_counter()}, " \
                f"Duration: {perf_counter() - start_time}"
            )

            output_file.close()
            log.info("Finished recording microphone audio!")
