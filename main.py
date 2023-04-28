import recorder_video as rv
import recorder_audio as ra
from encoder import Encoder

def main():

    MONITOR = 2
    # REGION = [0, 0, 1920, 1080]
    REGION = [60, 216, 1150, 650]
    DURATION = 3
    FPS = 30

    video_recorder = rv.VideoRecorder(
        monitor=MONITOR, 
        region=REGION,
        duration=DURATION,
        fps=FPS
    )

    audio_recorder = ra.AudioRecorder(
        duration=DURATION,
        loopback=True,
        microphone=False
    )

    video_recorder.start()
    audio_recorder.record()

    video_recorder.join()

    Encoder.merge_audio_clips(
        "AV-temp-audio.wav",
        "AV-temp-mic-audio.wav"
    )

    Encoder.merge_video_and_audio_moviePy(
        'AV-temp-video.mp4', 
        'AV-temp-merged.wav', 
        'AV-FINAL.mp4'
    )

    print("All done!")

if __name__ == '__main__':
    main()
