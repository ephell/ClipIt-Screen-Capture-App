import datetime
import os
import recorder_video as rv
import recorder_audio as ra
from encoder import Encoder

class Recorder:
    """Recording controller."""

    video_recorder = None
    audio_recorder = None

    def __init__(self, duration, record_loopback, record_microphone):
        self.duration = duration
        self.record_loopback = record_loopback
        self.record_microphone = record_microphone

        MONITOR = 2
        # REGION = [0, 0, 1920, 1080]
        REGION = [60, 216, 1150, 650]
        FPS = 30

        self.video_recorder = rv.VideoRecorder(
            monitor=MONITOR, 
            region=REGION,
            duration=self.duration,
            fps=FPS
        )

        if self.record_loopback or self.record_microphone:
            self.audio_recorder = ra.AudioRecorder(
                duration=self.duration,
                loopback=self.record_loopback,
                microphone=self.record_microphone
            )

    def record(self):
        if self.video_recorder is not None:
            self.video_recorder.start()
        if self.audio_recorder is not None:
            self.audio_recorder.record()
        self.video_recorder.join()

        self.__generate_final_video()
        self.__clean_up_temp_directory()

        print("All done!")

    def __generate_final_video(self):
        """Generates the final file from recorded temporary files."""
        if self.record_loopback and self.record_microphone:
            Encoder.merge_audio(
                first_clip="temp/TEMP-loopback.wav", 
                second_clip="temp/TEMP-microphone.wav", 
                output_path="temp/TEMP-merged.wav"
            )
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-merged.wav"
            )
        elif self.record_loopback and not self.record_microphone:
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-loopback.wav"
            )
        elif self.record_microphone and not self.record_loopback:
            Encoder.merge_video_with_audio(
                video_path="temp/TEMP-video.mp4",
                audio_path="temp/TEMP-microphone.wav"
            )
        else:
            os.replace("temp/TEMP-video.mp4", "temp/TEMP-Final.mp4")

        # Rename the final file and move it to output folder.
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d [] %H-%M-%S")
        filename = f"{timestamp}.mp4"
        os.rename("temp/TEMP-Final.mp4", f"recordings/{filename}")

    def __clean_up_temp_directory(self):
        """Removes all temporary files from the temp directory."""
        files = os.listdir("temp/")
        for file in files:
            if "TEMP-" in file:
                os.remove("temp/" + file)
