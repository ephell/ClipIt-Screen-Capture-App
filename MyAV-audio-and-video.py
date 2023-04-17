import numpy as np
from PIL import ImageGrab
import av
import multiprocessing as mp
import soundcard as sc
import soundfile as sf
import time

RECORD_SEC = 5

class VideoRecorder(mp.Process):

    def __init__(self):
        super().__init__()

    def run(self):
        print("Started video recording process ... ")

        container = av.open('AV-temp-video.mp4', mode='w')
        video_stream = container.add_stream('libx264', rate=30)
        video_stream.width = 1920
        video_stream.height = 1080

        fps = 30
        duration = RECORD_SEC
        num_frames = fps * duration

        for _ in range(num_frames):
            screen = np.array(ImageGrab.grab(bbox=(0, 0, 1920, 1080)))
            frame = av.VideoFrame.from_ndarray(screen, format='rgb24')
            packet = video_stream.encode(frame)
            if packet:
                container.mux(packet)

        video_stream.encode(None)
        container.close()

        print("Finished recording video!")


class AudioRecorder(mp.Process):
    
    SAMPLE_RATE = 48000

    def __init__(self):
        super().__init__()

    def run(self):
        print("Started audio recording process ... ")

        with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(samplerate=self.SAMPLE_RATE) as mic:
            self.audio_data = mic.record(numframes=self.SAMPLE_RATE*RECORD_SEC)
            sf.write("AV-temp-audio.wav", self.audio_data, self.SAMPLE_RATE)

        print("Finished recording audio!")

    
def add_audio_to_video(video_path, audio_path, output_path):
    # Open the input video and audio files
    video_container = av.open(video_path, 'r')
    audio_container = av.open(audio_path, 'r')

    # Open the output file
    output_container = av.open(output_path, 'w')

    # Get the video and audio streams
    video_stream = video_container.streams.video[0]
    audio_stream = audio_container.streams.audio[0]

    # Add the video and audio streams to the output container
    output_video_stream = output_container.add_stream(template=video_stream)
    output_audio_stream = output_container.add_stream(template=audio_stream)

    for packet in video_container.demux(video_stream):
        if packet.dts is None:
            continue
        packet.stream = output_video_stream
        output_container.mux(packet)

    for packet in audio_container.demux(audio_stream):
        if packet.dts is None:
            continue
        packet.stream = output_audio_stream
        output_container.mux(packet)

    # Flush and close the output container
    output_container.close()


def transcode_audio():

    input_file = "AV-temp-audio.wav"
    output_file = "AV-temp-audio-transcoded.mp4"

    input_container = av.open(input_file)
    input_audio_stream = input_container.streams.audio[0]

    output_container = av.open(output_file, mode='w')
    output_audio_stream = output_container.add_stream('aac', rate=input_audio_stream.rate)

    for packet in input_container.demux(input_audio_stream):
        for frame in packet.decode():
            # Encode the audio packet into the desired format
            encoded_packet = output_audio_stream.encode(frame)
            # Write the encoded packet to the output container
            output_container.mux(encoded_packet)

    # Flush the output container to ensure all packets are written
    output_container.close()


if __name__ == '__main__':

    video_recorder = VideoRecorder()
    audio_recorder = AudioRecorder()

    video_recorder.start()
    audio_recorder.start()

    video_recorder.join()
    audio_recorder.join()

    transcode_audio()
    add_audio_to_video('AV-temp-video.mp4', 'AV-temp-audio-transcoded.mp4', 'AV-FINAL.mp4')

    print("All done!")
