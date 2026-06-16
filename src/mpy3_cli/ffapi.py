import json
import subprocess
from pathlib import Path

from mpy3_cli.types import MediaInfo
from mpy3_cli.utils.constants import MILLISECONDS


def transcode_to_pipe(
    mrl: Path,
    format: str,
    codec: str,
    sample_rate: int,
    channels: int,
    start_time: int = 0,
) -> subprocess.Popen[bytes]:
    print("Starting transcoding process...")

    return subprocess.Popen(
        [
            "ffmpeg",
            "-ss",
            str(start_time / MILLISECONDS),
            "-i",
            str(mrl),
            "-f",
            format,
            "-acodec",
            codec,
            "-ar",
            str(sample_rate),
            "-ac",
            str(channels),
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )


def probe_media(mrl: Path) -> MediaInfo:
    print("Probing media file...")

    result = subprocess.run(
        ["ffprobe", "-i", str(mrl), "-v", "error", "-show_streams", "-of", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    result_json = result.stdout
    stream_info = dict(json.loads(result_json).get("streams", {})[0])
    return {
        "sample_rate": int(stream_info["sample_rate"]),
        "channels": stream_info["channels"],
    }


def probe_media_duration(mrl: Path) -> int:
    result = subprocess.run(
        [
            "ffprobe",
            "-i",
            str(mrl),
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    response_json = result.stdout
    duration_in_secs = float(
        json.loads(response_json).get("format", {}).get("duration", -1)
    )

    return int(duration_in_secs * 1000)


def probe_media_tags(mrl: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-i",
            str(mrl),
            "-v",
            "error",
            "-show_entries",
            "format_tags",
            "-of",
            "json",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    result_json = result.stdout
    tags = dict(json.loads(result_json).get("format", {}).get("tags", {}))
    return tags
