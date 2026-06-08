from mpy3_cli.audio_engine import AudioEngine
from mpy3_cli.media import Media


class PlaybackController:
    def __init__(self, media: Media) -> None:
        self.media = media
        self.engine: AudioEngine = AudioEngine(media)

        self.paused = self.engine.paused

    def play(self) -> None:
        self.engine.play()
        self.paused = self.engine.paused

    def pause(self) -> None:
        self.engine.pause()
        self.paused = self.engine.paused

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

    def get_time(self) -> int:
        return self.engine.get_time()
