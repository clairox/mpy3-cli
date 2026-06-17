from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static

from mpy3_cli.media import Media
from mpy3_cli.utils.constants import DEFAULT_ARTIST
from mpy3_cli.utils.timestr_from_ms import timestr_from_ms


class MediaListBrowser(Widget):
    DEFAULT_CSS = """
    MediaListBrowser {
        layout: vertical;
        height: auto;
    }
    """
    # TODO: Find less performance-intensive way to do this
    selected_media_idx = reactive(0, recompose=True)

    def __init__(self, media_list: list[Media]) -> None:
        super().__init__()

        self.media_list = media_list

    def compose(self) -> ComposeResult:
        for idx, media in enumerate(self.media_list):
            yield MediaListBrowserItem(
                media,
                classes=("selected" if self.selected_media_idx == idx else None),
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
        width: 90%;
    }

    MediaListBrowserItem > .right {
        content-align: right middle;
        width: 10%;
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
