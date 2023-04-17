import numpy as np
from PIL import ImageGrab
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
import soundcard as sc
import soundfile as sf
import numpy as np
import multiprocessing as mp

OUTPUT_FILE_NAME = "encoded-loopback.wav" # file name.
VIDEO_FILE_NAME = "main.mp4" # output video file name
SAMPLE_RATE = 48000 # [Hz]. sampling rate.
RECORD_SEC = 15 # [sec]. duration recording audio.

# Create a video recording process
class VideoRecorder(mp.Process):
    def __init__(self, frames):
        super().__init__()
        self.frames = frames

    def run(self):
        print("Started video recording process ... ")
        fps = 30
        duration = RECORD_SEC
        num_frames = fps * duration
        for _ in range(num_frames):
            screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            self.frames.append(screen)

# Create an audio recording process
class AudioRecorder(mp.Process):
    def __init__(self, audio_data):
        super().__init__()
        self.audio_data = audio_data

    def run(self):
        print("Started audio recording process ... ")
        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=SAMPLE_RATE) as mic:
            self.audio_data = mic.record(numframes=SAMPLE_RATE*RECORD_SEC)
            sf.write(OUTPUT_FILE_NAME, self.audio_data, SAMPLE_RATE)

if __name__ == '__main__':
    # Create shared memory to store video frames and audio data
    frames = mp.Manager().list()
    audio_data = mp.Manager().list()

    # Start both processes
    video_process = VideoRecorder(frames)
    audio_process = AudioRecorder(audio_data)
    audio_process.start()
    video_process.start()

    # Wait for both processes to finish
    video_process.join()
    audio_process.join()

    # Convert shared memory frames to regular list
    frames = list(frames)

    # Create video clip from frames and add audio
    clip = ImageSequenceClip(frames, fps=30)
    audio_clip = AudioFileClip(OUTPUT_FILE_NAME)
    new_audio_clip = CompositeAudioClip([audio_clip])
    clip.audio = new_audio_clip

    # Set the frame rate of the clip to match the audio
    clip.set_fps(SAMPLE_RATE)

    # Write video file
    clip.write_videofile(VIDEO_FILE_NAME)
