import time
from pathlib import Path

from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.events import Key

from mpy3_cli.event import event_manager
from mpy3_cli.ui.widgets.MediaListBrowser import MediaBrowser
from mpy3_cli.ui.widgets.PlayerPanel import PlayerPanel

KEY_DEBOUNCE_TIME = 0.0625


class App(TextualApp):
    def __init__(self, media_dir: Path) -> None:
        super().__init__()

        self.media_dir = media_dir

        # self.player = MediaPlayer(self.media_list[0])
        # self.pc = self.player.pc

        self.block_key_events_until = -1

        event_manager.attach("player_time_changed", self.on_time_update)

    def compose(self) -> ComposeResult:
        yield MediaBrowser(self.media_dir)

    def on_time_update(self, event) -> None:
        self.query_one(PlayerPanel).time = event.value

    def on_key(self, event: Key) -> None:
        if time.time() < self.block_key_events_until:
            return
        elif self.block_key_events_until >= 0:
            self.block_key_events_until = -1

        key = event.key

        if key == "q":
            # self.pc.stop()
            self.exit()

        # if key == "space":
        #     if not self.pc.paused:
        #         self.pc.pause()
        #         self.query_one(PlayerPanel).is_playing = False
        #     else:
        #         self.pc.play()
        #         self.query_one(PlayerPanel).is_playing = True
        #
        # if key == "right" or key == "l":
        #     self.pc.fast_forward()
        #
        # if key == "left" or key == "h":
        #     self.pc.rewind()

        self.block_key_events_until = time.time() + KEY_DEBOUNCE_TIME
