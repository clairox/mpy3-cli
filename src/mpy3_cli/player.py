import json
import subprocess
from pathlib import Path
from subprocess import Popen
from threading import Thread

import pyaudio
from pyaudio import PyAudio, Stream

CHUNK_SIZE = 1024


class Player:
    def __init__(self, mrl: Path) -> None:
        self.mrl = mrl
        self.format = "s16le"
        self.codec = "pcm_" + self.format

        stream_info = get_media_stream_info(self.mrl)
        self.sample_rate = stream_info["sample_rate"]
        self.channels = stream_info["channels"]

        self.input_stream: Popen[bytes] | None = None
        self.output_stream: Stream | None = None
        self.p: PyAudio = PyAudio()
        self.playback_thread: Thread | None = None

    def play(self) -> None:
        self.input_stream = start_media_stream(
            self.mrl, self.format, self.codec, self.sample_rate, self.channels
        )
        self.output_stream = self._open_stream()
        self.playback_thread = Thread(target=self._playback)
        self.playback_thread.start()

    def _playback(self) -> None:
        if self.input_stream is None:
            raise ValueError('"self.process" has not been set.')

        if self.input_stream.stdout is None:
            raise ValueError('"self.process.stdout" has not been set.')

        if self.output_stream is None:
            raise ValueError('"self.stream" has not been set.')

        print(f"Playing {self.mrl}")

        while True:
            data = self.input_stream.stdout.read(CHUNK_SIZE)
            if not data:
                print("Playback complete")
                break

            self.output_stream.write(data)

    def _open_stream(self) -> Stream:
        return self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            output=True,
        )


def start_media_stream(
    mrl: Path,
    format: str,
    codec: str,
    sample_rate: int,
    channels: int,
    start_time: int = 0,
) -> subprocess.Popen[bytes]:
    print("Starting ffmpeg process...")
    return subprocess.Popen(
        [
            "ffmpeg",
            "-ss",
            str(start_time),
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


def get_media_stream_info(mrl: Path) -> dict:
    print("Parsing stream information...")
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
