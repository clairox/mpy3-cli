from textual.app import RenderResult
from textual.widget import Widget

from mpy3_cli.media import Media
from mpy3_cli.utils.time_from_ms import time_from_ms

DEFAULT_ARTIST = "Unknown Artist"
DEFAULT_DURATION = "--:--"
DEFAULT_TIME = "0:00"


class PlayerPanel(Widget):
    def __init__(self, media: Media) -> None:
        super().__init__()
        self.media = media

        self.title = self.media.title
        self.artist = self.media.meta["artist"] if self.media.meta else DEFAULT_ARTIST
        self.duration = self.media.duration

    def render(self) -> RenderResult:
        duration_timestring = time_from_ms(self.duration)

        return (
            f"{str(self.media.title)} - Playing"
            + f"\n{self.artist}"
            + f"\n0:00 / {duration_timestring}"
        )
