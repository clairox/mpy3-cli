from pathlib import Path

from mpy3_cli import ffapi


class Media:
    def __init__(self, mrl: Path) -> None:
        self.mrl: Path = mrl
        self.title: str = mrl.stem
        self.duration: int = ffapi.probe_media_duration(self.mrl)
        self.meta: None | dict = None

    def parse_meta(self) -> None:
        self.meta = ffapi.probe_media_tags(self.mrl)

        if self.meta and self.meta["title"]:
            self.title = self.meta["title"]
