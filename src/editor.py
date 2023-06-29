from moviepy.editor import VideoFileClip


class Editor:

    @staticmethod
    def cut_and_save_video(cut_begin, cut_end, input_file, output_file):
        clip = VideoFileClip(input_file)
        inner_clip = clip.subclip(cut_begin, cut_end)
        inner_clip.write_videofile(output_file)
