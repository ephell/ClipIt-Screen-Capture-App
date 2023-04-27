import av
from fractions import Fraction
import math
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageSequenceClip

class Encoder:

    @staticmethod
    def merge_video_and_audio_moviePy(video_path, audio_path, output_path):
        print("Merging video and audio ... ")
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            output_path, 
            preset="ultrafast",
            logger=None
        )
        print("Merging done!")
