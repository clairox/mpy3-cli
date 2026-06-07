from pathlib import Path

from textual.app import App as TextualApp
from textual.app import ComposeResult, RenderResult
from textual.events import Key
from textual.widget import Widget

from mpy3_cli.playback import PlaybackController as PC


class App(TextualApp):
    def __init__(self, mrl: Path) -> None:
        super().__init__()
        self.mrl = mrl
        self.player = PC(self.mrl)

    def compose(self) -> ComposeResult:
        self.player.play()

        yield MediaInfoContainer(self.mrl)
        yield ProgressBar()

    def on_key(self, event: Key) -> None:
        if event.key == "q":
            self.player.stop()
            self.exit()


class MediaInfoContainer(Widget):
    def __init__(self, mrl: Path) -> None:
        super().__init__()
        self.mrl = mrl

    def render(self) -> RenderResult:
        return str(self.mrl.name) + "\nUnknown Artist" + "\n0:00 / 0:00"


class ProgressBar(Widget):
    def render(self) -> RenderResult:
        return ""
