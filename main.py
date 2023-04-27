import recorder_audio
import recorder_video
from encoder import Encoder
import recorder_video
from silence_player import SilencePlayer

def main():

    MONITOR = 2
    # REGION = [0, 0, 1920, 1080]
    REGION = [60, 216, 1150, 650]
    DURATION = 10
    FPS = 30

    video_recorder = recorder_video.VideoRecorder(
        monitor=MONITOR, 
        region=REGION,
        duration=DURATION,
        fps=FPS
    )

    audio_recorder = recorder_audio.AudioRecorder(
        DURATION
    )

    silence_player = SilencePlayer(duration=DURATION)

    video_recorder.start()
    silence_player.start()
    audio_recorder.start()

    video_recorder.join()
    audio_recorder.join()

    Encoder.merge_video_and_audio_moviePy(
        'AV-temp-video.mp4', 
        'AV-temp-audio.wav', 
        'AV-FINAL.mp4'
    )

    print("All done!")

if __name__ == '__main__':
    main()
