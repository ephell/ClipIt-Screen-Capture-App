import recorder_audio
import recorder_video
from encoder import Encoder

def main():

    RECORD_DURATION = 5

    video_recorder = recorder_video.VideoRecorder(
        monitor=2, 
        region=[0, 0, 1920, 1080],
        duration=RECORD_DURATION,
        fps=30
    )
    audio_recorder = recorder_audio.AudioRecorder(
        RECORD_DURATION, 
        sample_rate=44100
    )

    video_recorder.start()
    audio_recorder.start()

    video_recorder.join()
    audio_recorder.join()

    Encoder.transcode_audio()
    Encoder.add_audio_to_video(
        'AV-temp-video.mp4', 
        'AV-temp-audio-transcoded.mp4', 
        'AV-FINAL.mp4'
    )

    print("All done!")


if __name__ == '__main__':
    main()
