from textual.app import RenderResult
from textual.reactive import reactive
from textual.widget import Widget

from mpy3_cli.media import Media
from mpy3_cli.utils.constants import DEFAULT_ARTIST
from mpy3_cli.utils.timestr_from_ms import timestr_from_ms


class PlayerPanel(Widget):
    is_playing = reactive(False)
    time = reactive(0)

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
            + f"\n{timestr_from_ms(self.time)} / {duration_timestring}"
        )
