import multiprocessing as mp
from pydub import AudioSegment
from pydub.playback import play

class SilencePlayer(mp.Process):
    
    def __init__(self, duration):
        super().__init__()
        self.duration = duration + 5

    def run(self):
        print(f"Playing silence in the background for {self.duration} sec...")
        silence = AudioSegment.silent(
            duration=self.duration*1000,
            frame_rate=44100,
        )
        play(silence)
        print("Stopped playing silence!")
