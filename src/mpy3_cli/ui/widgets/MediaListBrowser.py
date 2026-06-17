from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from mpy3_cli.media import Media
from mpy3_cli.utils.constants import DEFAULT_ARTIST
from mpy3_cli.utils.timestr_from_ms import timestr_from_ms


class MediaListBrowser(Widget):
    selected_media_idx = reactive(0)

    def __init__(self, media_list: list[Media]) -> None:
        super().__init__()

        self.media_list = media_list

    def compose(self) -> ComposeResult:
        yield MediaListBrowserItem(
            self.media_list[0],
            classes=("selected" if self.selected_media_idx == 0 else None),
        )


class MediaListBrowserItem(Widget):
    DEFAULT_CSS = """
    MediaListBrowserItem {
        layout: horizontal;
        padding: 0 1;
        height: auto;
    }

    MediaListBrowserItem.selected {
        background: blue 50%;
    }

    MediaListBrowserItem > .left {
        content-align: left middle;
        width: 1fr;
    }

    MediaListBrowserItem > .right {
        content-align: right middle;
        width: 1fr;
    }
    """

    def __init__(self, media: Media, classes: None | str = None) -> None:
        super().__init__(classes=classes)

        self.title = media.title
        self.artist = media.meta["artist"] if media.meta else DEFAULT_ARTIST
        self.duration = media.duration

    def compose(self) -> ComposeResult:
        yield Static(f"{self.title} - {self.artist}", classes="left")
        yield Static(timestr_from_ms(self.duration), classes="right")
