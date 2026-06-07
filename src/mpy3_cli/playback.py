from pathlib import Path

from mpy3_cli.audio_engine import AudioEngine
from mpy3_cli.media import Media


class PlaybackController:
    def __init__(self, media: Media) -> None:
        self.media = media
        self.engine: AudioEngine = AudioEngine(media.mrl)

    def play(self) -> None:
        self.engine.play()

    def pause(self) -> None:
        pass

    def stop(self) -> None:
        self.engine.stop()

    def next(self) -> None:
        pass

    def previous(self) -> None:
        pass

    def fast_forward(self) -> None:
        pass

    def rewind(self) -> None:
        pass
