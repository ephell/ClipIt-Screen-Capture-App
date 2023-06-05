from moviepy.editor import VideoFileClip, concatenate_videoclips


class Editor:

    @staticmethod
    def cut_part_of_video(cut_begin, cut_end, input_file, output_file):
        clip = VideoFileClip(input_file)
        outer_clip_1 = clip.subclip(0, cut_begin)
        outer_clip_2 = clip.subclip(cut_end, clip.duration)
        trimmed_clip = concatenate_videoclips([outer_clip_1, outer_clip_2])
        trimmed_clip.write_videofile(output_file)
