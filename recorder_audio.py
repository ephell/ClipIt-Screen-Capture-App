import multiprocessing as mp
import pyaudiowpatch as pyaudio
import numpy as np
import time
import wave
import audioop

class AudioRecorder(mp.Process):
    
    filename = "AV-temp-audio.wav"

    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def run(self):
        print("Started audio recording process ... ")

        with pyaudio.PyAudio() as p:
            """Create PyAudio instance via context manager."""
            try:
                # Get default WASAPI info
                wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                print("WASAPI is not available on the system. Exiting...")
                exit()
            
            # Get default WASAPI speakers
            default_speakers = p.get_device_info_by_index(
                wasapi_info["defaultOutputDevice"]
            )

            if not default_speakers["isLoopbackDevice"]:
                for loopback in p.get_loopback_device_info_generator():
                    """
                    Try to find loopback device with same name
                    (and [Loopback suffix]).
                    """
                    if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        break
                else:
                    print("Default loopback output device not found.\n")
                    print("Run this to check available devices.\n")
                    print("Exiting...\n")
                    exit()
            
            FORMAT = pyaudio.paInt16
            CHANNELS = default_speakers["maxInputChannels"]
            RATE = int(default_speakers["defaultSampleRate"])
            SAMPLE_SIZE = pyaudio.get_sample_size(pyaudio.paInt16)

            waveFile = wave.open(self.filename, 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setframerate(RATE)
            waveFile.setsampwidth(SAMPLE_SIZE)

            # Open stream, capture data and write to file.
            with p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=SAMPLE_SIZE,
                input=True,
                input_device_index=default_speakers["index"],
            ) as stream:
                start_time = time.time()
                while time.time() - start_time <= self.duration:
                    in_data = stream.read(
                        stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    waveFile.writeframes(in_data)
                    
            waveFile.close()

        print("Finished audio recording process!")
