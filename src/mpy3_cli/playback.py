from pathlib import Path

from mpy3_cli.audio_engine import AudioEngine


class PlaybackController:
    def __init__(self, mrl: Path) -> None:
        self.engine: AudioEngine = AudioEngine(mrl)

    def play(self) -> None:
        self.engine.play()

    def pause(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def next(self) -> None:
        pass

    def previous(self) -> None:
        pass

    def fast_forward(self) -> None:
        pass

    def rewind(self) -> None:
        pass
