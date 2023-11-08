import multiprocessing as mp
from time import perf_counter, sleep

import imageio
import mss
import numpy as np

from src.settings.settings import Settings


class VideoRecorder(mp.Process):
    """Continuously captures specified region and saves to a video file."""

    def __init__(
            self, 
            region: list[int, int, int, int],
            monitor: int,
            fps: int,
            barrier: mp.Barrier=None,
            stop_event: mp.Event=None,
            reencoding_progress_queue: mp.Queue=None,
            recording_started: mp.Value=None, # Float value set to -1.0
            file_generation_choice_event: mp.Event=None,
            file_generation_choice_value: mp.Value=None,
        ):
        super().__init__()
        self.region = region
        self.monitor = monitor
        self.fps = fps
        self.barrier = barrier
        self.stop_event = stop_event
        self.reencoding_progress_queue = reencoding_progress_queue
        self.recording_started = recording_started
        self.file_generation_choice_event = file_generation_choice_event
        self.file_generation_choice_value = file_generation_choice_value
        self.captured_filename = Settings.get_temp_file_paths().CAPTURED_VIDEO_FILE
        self.reencoded_filename = Settings.get_temp_file_paths().REENCODED_VIDEO_FILE
        self.macro_block_size = 2
        self.quality = 5 # 10 is max (pretty large file size)
        self.__frame_writer_fps = 30 # Value doesn't matter since the video is going to be reencoded anyway

    def run(self):
        fps_counts = self.__capture_and_save_video()
        if self.file_generation_choice_event is not None:
            self.file_generation_choice_event.wait()
        if (
            self.file_generation_choice_value is None
            or self.file_generation_choice_value.value == True
        ):
            self.__reencode_video(fps_counts)

    def __capture_and_save_video(self):
        with mss.mss() as sct:
            monitor = {
                "left": int(self.region[0]),
                "top": int(self.region[1]),
                "width": int(self.region[2]),
                "height": int(self.region[3]),
                "mon": self.monitor,
            }

            frame_writer = imageio.get_writer(
                self.captured_filename,
                fps=self.__frame_writer_fps,
                quality=self.quality,
                macro_block_size=self.macro_block_size
            )

            # Syncing with other recording processes.
            if isinstance(self.barrier, mp.synchronize.Barrier):
                self.barrier.wait()
            else:
                print(
                    f"Barrier not set in: {self.__class__.__name__}. " \
                    "Final file might be out of sync."
                )

            print("Started recording video ... ")
            # Letting the main thread know that recording has started.
            start_time = perf_counter()
            if self.recording_started is not None:
                self.recording_started.value = start_time

            fps = 0
            fps_counts = []
            start_time = perf_counter()
            while not self.stop_event.is_set():
                frame = np.array(sct.grab(monitor))
                frame_writer.append_data(frame)
                fps += 1
                current_time = perf_counter()
                if current_time - start_time >= 1.0:
                    fps_counts.append(fps)
                    fps = 0
                    start_time = current_time

            frame_writer.close()
            print("Finished recording video!")

        return fps_counts

    def __reencode_video(self, fps_counts):
        """Rewrites the video file with precise fps."""
        print("Started reencoding video ... ")
        total_frames_in_input_file = sum(fps_counts)
        average_fps = int(sum(fps_counts) / len(fps_counts))
        self.fps = average_fps

        input_video_reader = imageio.get_reader(self.captured_filename)
        output_video_writer = imageio.get_writer(
            self.reencoded_filename,
            fps=self.fps,
            quality=self.quality,
            macro_block_size=self.macro_block_size
        )

        frames_written = 0
        for _, frame_count in enumerate(fps_counts):
            frames = self.__extract_frames(frame_count, input_video_reader)
            extended_frame_batch = self.__extend_frame_batch(frames, self.fps)
            for _, frame_data in extended_frame_batch.items():
                frame_data = self.__remove_alpha_channel(frame_data)
                frame_data = self.__flip_from_BGRA_to_RGB(frame_data)
                output_video_writer.append_data(frame_data)
                frames_written += 1
                if self.reencoding_progress_queue is not None:
                    progress = (frames_written / total_frames_in_input_file) * 100
                    self.reencoding_progress_queue.put(progress)

        input_video_reader.close()
        output_video_writer.close()
        print("Finished reencoding video!")

    def __extract_frames(self, frame_amount, input_video_reader):
        frames = {}
        for frame_index in range(frame_amount):
            frame_data = input_video_reader.get_next_data()
            if frame_data is None:
                break
            frames.update({frame_index: frame_data})
        return frames
    
    def __extend_frame_batch(self, frames: dict[int, np.ndarray], extend_to_fps):
        """
        Extend a dictionary of frames to match the specified fps.
        
        It fills the gaps between the frames by duplicating where
        needed. In the case where `extend_to_fps` is smaller than
        the amount of frames, some middle frames will be skipped in
        the resulting dictionary.
        """
        extended_batch = {}
        frames_per_source_frame = extend_to_fps / len(frames)
        for i in range(extend_to_fps):
            src_frame = int(i / frames_per_source_frame)
            extended_batch[i] = frames[src_frame]
        return extended_batch

    def __remove_alpha_channel(self, frame: np.ndarray):
        return frame[:, :, :3]

    def __flip_from_BGRA_to_RGB(self, frame: np.ndarray):
        return np.flip(frame[:, :, :3], 2)
