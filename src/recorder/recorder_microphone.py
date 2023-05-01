from settings import Paths, TempFiles, GlobalLogger
log = GlobalLogger.LOGGER

import multiprocessing as mp
from time import perf_counter
import wave

import pyaudiowpatch as pyaudio


class MicrophoneRecorder(mp.Process):
    """Records audio from the default microphone."""

    def __init__(self, microphone, duration, barrier=None):
        super().__init__()
        self.duration = duration
        self.barrier = barrier
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
                
                if isinstance(self.barrier, mp.synchronize.Barrier):
                    self.barrier.wait()
                else:
                    log.warning(f"Barrier not set in: {self.__class__.__name__}. " \
                                "Final audio file might be out of sync.")

                log.info("Started recording microphone audio ... ")

                start_time = perf_counter()
                while perf_counter() - start_time < self.duration:
                    data = stream.read(
                        num_frames=stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)

            output_file.close()

            log.info("Finished recording microphone audio!")
