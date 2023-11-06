import pyaudiowpatch as pyaudio


class AudioUtils:
    """Utility class for audio related methods."""

    @classmethod
    def get_default_speakers(cls):
        if cls.is_WASAPI_available():
            with pyaudio.PyAudio() as p:
                w = cls.get_WASAPI_info()
                try:
                    return p.get_device_info_by_index(w["defaultOutputDevice"])
                except OSError:
                    return None
        return None

    @classmethod
    def get_default_loopback_device(cls):
        default_speakers = AudioUtils.get_default_speakers()
        if default_speakers is not None:
            with pyaudio.PyAudio() as p:
                for loopback_device in p.get_loopback_device_info_generator():
                    if default_speakers["name"] in loopback_device["name"]:
                        return loopback_device
        return None

    @classmethod
    def get_WASAPI_info(cls):
        with pyaudio.PyAudio() as p:
            try:
                return p.get_host_api_info_by_type(pyaudio.paWASAPI)
            except OSError:
                return False

    @classmethod
    def is_WASAPI_available(cls):
        with pyaudio.PyAudio() as p:
            host_apis = p.get_host_api_info_generator()
            for api in host_apis:
                if "wasapi" in api["name"].lower():
                    return True
            return False
