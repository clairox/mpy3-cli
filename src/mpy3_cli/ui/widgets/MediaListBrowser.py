from pathlib import Path
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import ListItem, ListView, Static

from mpy3_cli.media import Media
from mpy3_cli.utils.constants import DEFAULT_ARTIST
from mpy3_cli.utils.timestr_from_ms import timestr_from_ms

ACCEPTED_FILE_TYPES = [".mp3"]


class MediaBrowser(Widget):

    def __init__(self, dir: Path) -> None:
        super().__init__()

        paths = sorted(Path(dir).iterdir())
        valid_paths = [
            p for p in paths if p.is_file() and p.suffix in ACCEPTED_FILE_TYPES
        ]
        self.media_list: list[Media] = [Media(p) for p in valid_paths]
        for media in self.media_list:
            media.parse_meta()

    def compose(self) -> ComposeResult:
        items = []
        for idx, media in enumerate(self.media_list):
            classes = "even" if idx % 2 == 0 else "odd"

            items.append(MediaBrowserItem(media, False, classes=classes))

        yield MediaBrowserList(*items)


class MediaBrowserList(ListView):
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
    ]

    def __init__(self, *children: MediaBrowserItem) -> None:
        super().__init__(*children, initial_index=0)

        self.focus()


class MediaBrowserItem(ListItem):
    DEFAULT_CSS = """
    MediaBrowserItem {
        layout: horizontal;
        padding: 0 1;
        height: auto;
    }

    MediaBrowserItem.even {
        background: gray 15%;
    }

    MediaBrowserItem.selected {
        background: #0186cc;
    }

    MediaBrowserItem > .left {
        content-align: left middle;
        width: 90%;
    }

    MediaBrowserItem > .right {
        content-align: right middle;
        width: 10%;
    }
    """

    is_selected = reactive(False, recompose=True)

    def __init__(
        self, media: Media, is_selected: bool, classes: None | str = None
    ) -> None:
        super().__init__(classes=classes)

        self.is_selected = is_selected
        if self.is_selected:
            self.add_class("selected")

        self.title = media.title
        self.artist = DEFAULT_ARTIST
        if media.meta:
            media.meta.get("artist", DEFAULT_ARTIST)
        self.duration = media.duration

    def compose(self) -> ComposeResult:
        yield Static(f"{self.title} - {self.artist}", classes="left")
        yield Static(timestr_from_ms(self.duration), classes="right")
