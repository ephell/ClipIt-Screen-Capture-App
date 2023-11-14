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
        self.fps_limit = 30

    def run(self):
        fps_counts = self.__capture_and_save_frames()
        if self.file_generation_choice_event is not None:
            self.file_generation_choice_event.wait()
        if (
            self.file_generation_choice_value is None
            or self.file_generation_choice_value.value == True
        ):
            self.__reencode_captured_frames(fps_counts)

    def __capture_and_save_frames(self):
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
                fps=self.fps_limit,
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
                frame_start_time = perf_counter()
                frame = np.array(sct.grab(monitor))
                frame_writer.append_data(frame)
                fps += 1
                current_time = perf_counter()
                if current_time - start_time >= 1.0:
                    fps_counts.append(fps)
                    fps = 0
                    start_time = current_time

                # Limiting the fps
                frame_capture_time = perf_counter() - frame_start_time
                sleep_time = (1.0 / self.fps_limit) - frame_capture_time
                if sleep_time > 0:
                    sleep(sleep_time)

            # Appending the fps count of the last second
            if fps > 0:
                fps_counts.append(fps)

            frame_writer.close()
            print("Finished recording video!")

        return fps_counts

    def __reencode_captured_frames(self, fps_counts):
        print("Started reencoding video ... ")
        input_video_reader = imageio.get_reader(self.captured_filename)
        output_video_writer = imageio.get_writer(
            self.reencoded_filename,
            fps=self.fps_limit,
            quality=self.quality,
            macro_block_size=self.macro_block_size
        )

        frame_batches_written = 0
        frame_batches_total = len(fps_counts)
        for i, frame_count in enumerate(fps_counts):
            extracted_frames = self.__extract_frames(frame_count, input_video_reader)
            if i != frame_batches_total - 1:
                frame_batch = self.__extend_to_fps_limit(extracted_frames)
            else:
                frame_batch = extracted_frames

            for _, frame_data in frame_batch.items():
                frame_data = self.__remove_alpha_channel(frame_data)
                frame_data = self.__flip_from_BGRA_to_RGB(frame_data)
                output_video_writer.append_data(frame_data)
            frame_batches_written += 1
            
            if self.reencoding_progress_queue is not None:
                progress = (frame_batches_written / frame_batches_total) * 100
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
    
    def __extend_to_fps_limit(self, frames: dict[int, np.ndarray]):
        """
        Extend the number of frames to the fps limit by duplicating
        where necessary.
        """
        extended_frames = {}
        frames_per_source_frame = self.fps_limit / len(frames)
        for i in range(self.fps_limit):
            extended_frames[i] = frames[int(i / frames_per_source_frame)]
        return extended_frames

    def __remove_alpha_channel(self, frame: np.ndarray):
        return frame[:, :, :3]

    def __flip_from_BGRA_to_RGB(self, frame: np.ndarray):
        return np.flip(frame[:, :, :3], 2)
