from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Encoder:
    """Holds methods for encoding audio and video files."""

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

    @staticmethod
    def merge_audio_clips(first_audio, second_audio):
        clip1 = AudioFileClip(first_audio)
        clip2 = AudioFileClip(second_audio)
        merged_audio = CompositeAudioClip([clip1, clip2])
        merged_audio.write_audiofile("AV-temp-merged.wav", fps=44100)
        