from mpy3_cli.audio_engine import AudioEngine

SEEK_INTERVAL = 5000


class PlaybackController:
    def __init__(self, engine: AudioEngine) -> None:
        self._engine = engine

        self.paused = self._engine.paused

    def play(self) -> None:
        self._engine.play()
        self.paused = self._engine.paused

    def pause(self) -> None:
        self._engine.pause()
        self.paused = self._engine.paused

    def stop(self) -> None:
        self._engine.stop()

    def fast_forward(self) -> None:
        self._engine.seek(self._engine.get_time() + SEEK_INTERVAL)

    def rewind(self) -> None:
        self._engine.seek(self._engine.get_time() - SEEK_INTERVAL)

    def next(self) -> None:
        pass

    def previous(self) -> None:
        pass
