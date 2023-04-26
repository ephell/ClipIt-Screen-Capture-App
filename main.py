import recorder_audio
import recorder_video
from encoder import Encoder
import recorder_video_moviePy

def main():

    MONITOR = 2
    # REGION = [0, 0, 1920, 1080]
    REGION = [60, 216, 1150, 650]
    DURATION = 10

    # video_recorder = recorder_video_moviePy.VideoRecorder(
    #     monitor=MONITOR, 
    #     region=REGION,
    #     duration=DURATION
    # )

    video_recorder = recorder_video.VideoRecorder(
        monitor=MONITOR, 
        region=REGION,
        duration=DURATION,
    )

    audio_recorder = recorder_audio.AudioRecorder(
        DURATION
    )

    video_recorder.start()
    audio_recorder.start()

    video_recorder.join()
    audio_recorder.join()

    Encoder.transcode_audio()
    # Encoder.add_audio_to_video(
    #     'AV-temp-video.mp4', 
    #     'AV-temp-audio-transcoded.mp4', 
    #     'AV-FINAL.mp4'
    # )

    Encoder.merge_video_and_audio_moviePy(
        'AV-temp-video.mp4', 
        'AV-temp-audio-transcoded.mp4', 
        'AV-FINAL.mp4'
    )

    print("All done!")

if __name__ == '__main__':
    main()
