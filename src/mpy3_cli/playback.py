from mpy3_cli.audio_engine import AudioEngine


class PlaybackController:
    def __init__(self, engine: AudioEngine) -> None:
        self.__engine = engine

        self.paused = self.__engine.paused

    def play(self) -> None:
        self.__engine.play()
        self.paused = self.__engine.paused

    def pause(self) -> None:
        self.__engine.pause()
        self.paused = self.__engine.paused

    def stop(self) -> None:
        self.__engine.stop()

    def fast_forward(self) -> None:
        pass

    def rewind(self) -> None:
        pass

    def next(self) -> None:
        pass

    def previous(self) -> None:
        pass
