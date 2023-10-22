import imageio
from moviepy.editor import VideoFileClip
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import numpy as np

from settings.settings import Settings


class VideoUtils:
    """Utility class for video operations."""

    @staticmethod
    def render_and_save_video(
        input_file_path,
        output_file_path,
        cut_begin: float=None, # in seconds
        cut_end: float=None, # in seconds
        volume: float=None, # 1.0 is 100%; None = keep original volume
        crop_area: tuple=None, # (x1, y1, x2, y2)
        logger=None,
        preset="ultrafast" # Impacts rendering speed (faster = bigger file size)
    ):
        base_video_clip = VideoFileClip(input_file_path)

        cut_begin = cut_begin if cut_begin is not None else 0.0
        cut_end = cut_end if cut_end is not None else base_video_clip.duration
        final_video_clip = base_video_clip.subclip(cut_begin, cut_end)

        if (
            crop_area is not None
            and not VideoUtils.is_crop_area_full_frame(crop_area, final_video_clip.get_frame(0))
        ):
            final_video_clip.write_videofile(
                filename=Settings.get_temp_file_paths().CUT_VIDEO_FILE,
                preset=preset,
                logger=logger.temp_cut_video_rendering
            )
            VideoUtils.crop_video(
                Settings.get_temp_file_paths().CUT_VIDEO_FILE,
                Settings.get_temp_file_paths().CROPPED_VIDEO_FILE,
                crop_area,
                logger=logger.cropping
            )
            cropped_video_clip = VideoFileClip(Settings.get_temp_file_paths().CROPPED_VIDEO_FILE)
            cut_audio_clip = VideoFileClip(Settings.get_temp_file_paths().CUT_VIDEO_FILE).audio
            final_video_clip = cropped_video_clip.set_audio(cut_audio_clip)

        if volume is not None:
            final_video_clip = final_video_clip.volumex(volume)

        final_video_clip.write_videofile(
            filename=output_file_path,
            preset=preset,
            logger=logger.final_file_rendering
        )

    @staticmethod
    def is_crop_area_full_frame(crop_area: tuple, frame: np.ndarray):
        """Returns True if the crop area is the same size as the frame."""
        if crop_area[0] > 0 or crop_area[1] > 0:
            return False
        frame_w, frame_h = frame.shape[1], frame.shape[0]
        crop_area_w = crop_area[2]
        crop_area_h = crop_area[3]
        if crop_area_w != frame_w or crop_area_h != frame_h:
            return False
        return True

    @staticmethod
    def crop_video(
        input_file_path, 
        output_file_path, 
        crop_area,
        logger=None
    ):
        reader = imageio.get_reader(input_file_path)
        writer = imageio.get_writer(
            output_file_path, 
            fps=reader.get_meta_data()["fps"], 
            quality=5,
            macro_block_size=2
        )
        total_frames = reader.count_frames()
        frames_processed = 0
        for frame in reader:
            cropped_frame = frame[
                crop_area[1]:crop_area[3], 
                crop_area[0]:crop_area[2]
            ]
            writer.append_data(cropped_frame)
            frames_processed += 1
            if logger is not None:
                progress = (frames_processed / total_frames) * 100
                logger.progress_signal.emit(progress)

        reader.close()
        writer.close()

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
