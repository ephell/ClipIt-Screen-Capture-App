import multiprocessing as mp
from time import perf_counter
import wave

import pyaudiowpatch as pyaudio

from src.settings.settings import Settings


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
                f=Settings.get_temp_file_paths().MICROPHONE_AUDIO_FILE,
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
                    print(
                        f"Barrier not set in: {self.__class__.__name__}. " \
                        "Final file might be out of sync."
                    )

                print("Started recording microphone audio ... ")
                start_time = perf_counter()
                while not self.stop_event.is_set():
                    data = stream.read(
                        num_frames=stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    output_file.writeframes(data)

            print(
                f"Stopped recording microphone audio at: {perf_counter()}, " \
                f"Duration: {perf_counter() - start_time}"
            )

            output_file.close()
            print("Finished recording microphone audio!")
