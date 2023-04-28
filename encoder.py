from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class Encoder:
    """Holds methods for encoding audio and video files."""

    @staticmethod
    def merge_video_with_audio(video_path, audio_path):
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            filename="temp/TEMP-Final.mp4",
            preset="ultrafast",
            logger=None
        )

    @staticmethod
    def merge_audio(first_clip, second_clip, output_path):
        clip1 = AudioFileClip(first_clip)
        clip2 = AudioFileClip(second_clip)
        merged_audio = CompositeAudioClip([clip1, clip2])
        merged_audio.write_audiofile(
            filename=output_path,
            fps=44100,
            logger=None
        )
