from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


class VideoUtils:
    """Utility class for video operations."""

    @staticmethod
    def cut_and_save_video(
        cut_begin, 
        cut_end, 
        input_file_path,
        output_file_path,
        logger=None
    ):
        clip = VideoFileClip(input_file_path)
        inner_clip = clip.subclip(cut_begin, cut_end)
        inner_clip.write_videofile(
            output_file_path,
            preset="ultrafast",
            logger=logger
        )
        
    @staticmethod
    def merge_video_with_audio(
        video_path, 
        audio_path,
        output_path, 
        logger=None
    ):
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(
            filename=output_path,
            preset="ultrafast",
            logger=logger
        )

    @staticmethod
    def merge_audio(
        first_clip_path, 
        second_clip_path,
        output_path,
        logger=None
    ):
        clip1 = AudioFileClip(first_clip_path)
        clip2 = AudioFileClip(second_clip_path)
        merged_audio = CompositeAudioClip([clip1, clip2])
        merged_audio.write_audiofile(
            filename=output_path,
            fps=44100,
            logger=logger
        )