import av

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

