from pathlib import Path
from typing import Any

from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.events import Key

from mpy3_cli.event import event_manager
from mpy3_cli.media import Media
from mpy3_cli.player import MediaPlayer
from mpy3_cli.ui.widgets.PlayerPanel import PlayerPanel


class App(TextualApp):
    def __init__(self, mrl: Path) -> None:
        super().__init__()
        self.media = Media(mrl)
        self.media.parse_meta()

        self.player = MediaPlayer(self.media)
        self.pc = self.player.pc

        event_manager.attach("player_time_changed", self.on_time_update)

    def compose(self) -> ComposeResult:
        self.pc.play()

        yield PlayerPanel(self.media)

    def on_time_update(self, event) -> None:
        self.query_one(PlayerPanel).time = event.value

    def on_key(self, event: Key) -> None:
        if event.key == "q":
            self.pc.stop()
            self.exit()

        if event.key == "space":
            if not self.pc.paused:
                self.pc.pause()
                self.query_one(PlayerPanel).is_playing = False
            else:
                self.pc.play()
                self.query_one(PlayerPanel).is_playing = True
