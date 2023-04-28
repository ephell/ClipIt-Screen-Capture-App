import multiprocessing as mp
import pyaudiowpatch as pyaudio
import time
import wave

class MicrophoneRecorder(mp.Process):
    
    def __init__(self, duration):
        super().__init__()
        self.duration = duration

    def get_default_microphone(self):
        with pyaudio.PyAudio() as p:
            try:
                info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                print("WASAPI not available on your system.")

            try:
                return p.get_device_info_by_index(info["defaultInputDevice"])
            except OSError:
                print("Default microphone not found.")

    def record_microphone(self):
        microphone = self.get_default_microphone()
        if not microphone:
            print("No microphone found, can't record.")
            return
        with pyaudio.PyAudio() as p:
            
            FORMAT = pyaudio.paInt16
            CHANNELS = microphone["maxInputChannels"]
            RATE = int(microphone["defaultSampleRate"])
            SAMPLE_SIZE = pyaudio.get_sample_size(pyaudio.paInt16)

            waveFile = wave.open("AV-temp-mic-audio.wav", 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setframerate(RATE)
            waveFile.setsampwidth(SAMPLE_SIZE)

            with p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                frames_per_buffer=SAMPLE_SIZE,
                input=True,
                input_device_index=microphone["index"],
            ) as stream:
                start_time = time.time()
                while time.time() - start_time <= self.duration:
                    data = stream.read(
                        stream.get_read_available(), 
                        exception_on_overflow=False
                    )
                    waveFile.writeframes(data)

            waveFile.close()

    def run(self):
        print("Started microphone recording process ... ")
        self.record_microphone()
        print("Finished microphone recording process!")
