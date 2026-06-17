import sys
from pathlib import Path

import click

from mpy3_cli.ui.app import App


@click.command()
@click.argument("media_dir_input")
def main(media_dir_input: str):
    media_dir = Path(media_dir_input)

    if not media_dir.exists() or not media_dir.is_dir():
        print(f"{media_dir} is not a valid directory.")
        sys.exit(1)

    app = App(media_dir)
    app.run()
