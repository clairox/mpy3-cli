import sys
import click
from pathlib import Path
    
ACCEPTED_FILE_TYPES = [".mp3"]

@click.command()
@click.argument("media_url_input")
def main(media_url_input: str):
    media_url = Path(media_url_input)

    if not media_url.exists() or not media_url.is_file():
        print(f"{media_url} is not a valid file.")
        sys.exit(1)

    if media_url.suffix not in ACCEPTED_FILE_TYPES:
        print(f"{media_url} is not an mp3 file.")
        sys.exit(1)

    print(f"{media_url} is a valid mp3 file!")


