from mpy3_cli.audio_engine import AudioEngine
from mpy3_cli.media import Media
from mpy3_cli.playback import PlaybackController


class MediaPlayer:
    def __init__(self, media: Media) -> None:
        self.media = media
        self.__engine = AudioEngine(self.media)
        self.pc = PlaybackController(self.__engine)
