import av
from fractions import Fraction
import math
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageSequenceClip

class Encoder:

    @staticmethod
    def add_audio_to_video(video_path, audio_path, output_path):
        # Open the input video and audio files
        video_container = av.open(video_path, 'r')
        audio_container = av.open(audio_path, 'r')

        # Open the output file
        output_container = av.open(output_path, 'w')

        # Get the video and audio streams
        video_stream = video_container.streams.video[0]
        audio_stream = audio_container.streams.audio[0]

        # video_stream.time_base = Fraction(1, 15)

        # Add the video and audio streams to the output container
        output_video_stream = output_container.add_stream(template=video_stream)
        output_audio_stream = output_container.add_stream(template=audio_stream)

        all_frame_times = []
        for packet in audio_container.demux(audio_stream):
            for frame in packet.decode():
                all_frame_times.append(frame.time)
            if packet.dts is None:
                continue
            packet.stream = output_audio_stream
            output_container.mux(packet)

        differences = [all_frame_times[i+1]-all_frame_times[i] for i in range(len(all_frame_times)-1)]
        avg_video_frame_time = sum(differences)/len(differences)
        avg_video_frame_rate = math.floor(1 / avg_video_frame_time)

        output_video_stream.rate = Fraction(avg_video_frame_rate, 1)

        for packet in video_container.demux(video_stream):
            if packet.dts is None:
                continue
            packet.stream = output_video_stream
            output_container.mux(packet)

        # Flush and close the output container
        # for out_packet in output_video_stream.encode(None):
        #     output_container.mux(out_packet)

        # for out_packet in output_audio_stream.encode(None):
        #     output_container.mux(out_packet)

        audio_container.close()
        video_container.close()
        output_container.close()

    @staticmethod
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


    @staticmethod
    def merge_video_and_audio_moviePy(video_path, audio_path, output_path):
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path)
