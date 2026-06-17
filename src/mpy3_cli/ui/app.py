import time
from pathlib import Path

from textual.app import App as TextualApp
from textual.app import ComposeResult
from textual.events import Key

from mpy3_cli.event import event_manager
from mpy3_cli.media import Media
from mpy3_cli.player import MediaPlayer
from mpy3_cli.ui.widgets.MediaListBrowser import MediaListBrowser
from mpy3_cli.ui.widgets.PlayerPanel import PlayerPanel

KEY_DEBOUNCE_TIME = 0.0625
ACCEPTED_FILE_TYPES = [".mp3"]


class App(TextualApp):
    def __init__(self, media_dir: Path) -> None:
        super().__init__()

        self.media_dir = media_dir
        self.media_list: list[Media] = [
            Media(m) for m in self._load_mrls(self.media_dir)
        ]
        for media in self.media_list:
            media.parse_meta()

        self.player = MediaPlayer(self.media_list[0])
        self.pc = self.player.pc

        self.block_key_events_until = -1

        event_manager.attach("player_time_changed", self.on_time_update)

    def compose(self) -> ComposeResult:
        yield MediaListBrowser(self.media_list)

    def on_time_update(self, event) -> None:
        self.query_one(PlayerPanel).time = event.value

    def on_key(self, event: Key) -> None:
        if time.time() < self.block_key_events_until:
            return
        elif self.block_key_events_until >= 0:
            self.block_key_events_until = -1

        key = event.key

        if key == "q":
            self.pc.stop()
            self.exit()

        if key == "space":
            if not self.pc.paused:
                self.pc.pause()
                self.query_one(PlayerPanel).is_playing = False
            else:
                self.pc.play()
                self.query_one(PlayerPanel).is_playing = True

        if key == "right" or key == "l":
            self.pc.fast_forward()

        if key == "left" or key == "h":
            self.pc.rewind()

        if key == "down" or key == "j":
            current_idx = self.query_one(MediaListBrowser).selected_media_idx
            new_idx = current_idx + 1

            if new_idx >= len(self.media_list):
                new_idx = len(self.media_list) - 1
            else:
                self.query_one(MediaListBrowser).selected_media_idx = new_idx

        if key == "up" or key == "k":
            current_idx = self.query_one(MediaListBrowser).selected_media_idx
            new_idx = current_idx - 1

            if new_idx < 0:
                new_idx = 0
            else:
                self.query_one(MediaListBrowser).selected_media_idx = new_idx

        self.block_key_events_until = time.time() + KEY_DEBOUNCE_TIME

    def _load_mrls(self, media_dir: Path) -> list[Path]:
        paths = sorted(Path(media_dir).iterdir())[:20]

        def is_valid_file(p: Path) -> bool:
            return p.is_file() and p.suffix in ACCEPTED_FILE_TYPES

        return [p for p in paths if is_valid_file(p)]
