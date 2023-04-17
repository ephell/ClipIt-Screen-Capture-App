import soundcard as sc
import soundfile as sf
import multiprocessing as mp

class AudioRecorder(mp.Process):
    
    def __init__(self, record_duration, sample_rate):
        super().__init__()
        self.record_duration = record_duration
        self.sample_rate = sample_rate

    def run(self):
        print("Started audio recording process ... ")

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.sample_rate) as mic:
            self.audio_data = mic.record(numframes=self.sample_rate*self.record_duration)
            sf.write("AV-temp-audio.wav", self.audio_data, self.sample_rate)

        print("Finished recording audio!")