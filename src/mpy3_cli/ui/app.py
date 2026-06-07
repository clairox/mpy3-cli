from pathlib import Path

from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.events import Key

from mpy3_cli.media import Media
from mpy3_cli.playback import PlaybackController as PC
from mpy3_cli.ui.widgets.PlayerPanel import PlayerPanel


class App(TextualApp):
    def __init__(self, mrl: Path) -> None:
        super().__init__()
        self.media = Media(mrl)
        self.media.parse_meta()

        self.player = PC(self.media)

    def compose(self) -> ComposeResult:
        self.player.play()

        yield PlayerPanel(self.media)

    def on_key(self, event: Key) -> None:
        if event.key == "q":
            self.player.stop()
            self.exit()
