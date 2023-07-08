from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from settings import Paths, TempFiles


class Merger:

    @staticmethod
    def merge_video_with_audio(video_path, audio_path, logger=None):
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            filename=f"{Paths.TEMP_DIR}/{TempFiles.FINAL_FILE}",
            preset="ultrafast",
            logger=logger
        )

    @staticmethod
    def merge_audio(first_clip, second_clip, logger=None):
        clip1 = AudioFileClip(first_clip)
        clip2 = AudioFileClip(second_clip)
        merged_audio = CompositeAudioClip([clip1, clip2])
        merged_audio.write_audiofile(
            filename=f"{Paths.TEMP_DIR}/{TempFiles.MERGED_AUDIO_FILE}",
            fps=44100,
            logger=logger
        )
