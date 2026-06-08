from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget

from mpy3_cli.media import Media
from mpy3_cli.utils.timestr_from_ms import timestr_from_ms

DEFAULT_ARTIST = "Unknown Artist"
DEFAULT_DURATION = "--:--"
DEFAULT_TIME = "0:00"


class PlayerPanel(Widget):
    is_playing = reactive(True)
    current_time = reactive(0)

    def __init__(self, media: Media) -> None:
        super().__init__()
        self.media = media

        self.title = self.media.title
        self.artist = self.media.meta["artist"] if self.media.meta else DEFAULT_ARTIST
        self.duration = self.media.duration

    def render(self) -> RenderResult:
        duration_timestring = timestr_from_ms(self.duration)

        return (
            f"{str(self.media.title)} - {"Playing" if self.is_playing else "Paused"}"
            + f"\n{self.artist}"
            + f"\n{timestr_from_ms(self.current_time)} / {duration_timestring}"
        )
