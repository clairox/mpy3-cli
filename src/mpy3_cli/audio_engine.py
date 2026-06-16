import math
import time as t
from subprocess import Popen
from threading import Thread

import pyaudio  # type: ignore
from pyaudio import PyAudio  # type: ignore
from pyaudio import Stream as PyAudioStream  # type: ignore

from mpy3_cli import ffapi
from mpy3_cli.event import event_manager
from mpy3_cli.media import Media
from mpy3_cli.types import MediaInfo
from mpy3_cli.utils.constants import BYTE, MILLISECONDS
from mpy3_cli.utils.get_system_time import get_system_time
from mpy3_cli.utils.no_alsa_err import no_alsa_err

CHUNK_SIZE = 1024

DEFAULT_BIT_DEPTH = 16
DEFAULT_FORMAT = f"s{DEFAULT_BIT_DEPTH}le"
DEFAULT_CODEC = "pcm_s16le"
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 2


class AudioEngine:
    """Handles media playback"""

    def __init__(self, media: Media) -> None:
        self.media = media
        self.mrl = self.media.mrl

        self.event_manager = event_manager

        self._input: InputStream | None = None
        self._output: OutputStream | None = None
        self._playback_thread: Thread | None = None

        with no_alsa_err():
            self._p: PyAudio = PyAudio()

        self.media_info: MediaInfo = ffapi.probe_media(self.mrl)

        self.bit_depth = DEFAULT_BIT_DEPTH
        self.format = DEFAULT_FORMAT
        self.codec = DEFAULT_CODEC
        self.bytes_per_sample: int = int(self.bit_depth / BYTE)

        self.paused = False
        self.stopped = False

        self.start_time: int | None = None
        self.bytes_transcoded = 0
        self.time = 0

    def play(self) -> None:
        if self._input is None:
            self._open_input_stream()
        elif self.paused:
            self.paused = False

    def pause(self) -> None:
        if self._input and not self.paused:
            self.paused = True

    def stop(self) -> None:
        if self._input and not self.stopped:
            self.stopped = True

    def get_time(self) -> int:
        if not self.start_time:
            return 0

        elapsed_time = get_system_time() - self.start_time

        current_sample = self.bytes_transcoded / (
            self.media_info["channels"] * self.bytes_per_sample
        )
        time_from_bytes = math.floor(
            (current_sample / self.media_info["sample_rate"]) * MILLISECONDS
        )

        return clamp(time_from_bytes, elapsed_time, self.media.duration)

    def _playback(self) -> None:
        if self._input is None:
            raise ValueError('"self._input" has not been set.')

        if self._output is None:
            raise ValueError('"self._output" has not been set.')

        print(f"Playing {self.mrl}")

        while True:
            if self.stopped:
                print("Playback stopped")
                break

            if self.paused:
                continue

            data = self._input.read(CHUNK_SIZE)
            if not data:
                print("Playback complete")
                break

            self._output.write(data)
            self.bytes_transcoded += len(data)

            new_time = self.get_time()
            if new_time > self.time:
                self.time = new_time
                self.event_manager.dispatch("player_time_changed", self.time)

    def _start_file_transcoding_process(self) -> None:
        """Begin streaming bytes from media file into a pipe"""

        process = ffapi.transcode_to_pipe(
            self.mrl,
            self.format,
            self.codec,
            self.media_info["sample_rate"],
            self.media_info["channels"],
        )

        self._input = InputStream(process)

    def _open_input_stream(self) -> None:
        """Setup input stream for playback"""

        self._start_file_transcoding_process()
        self._open_output_stream()
        self.start_time = system_time()
        self._playback_thread = Thread(target=self._playback)
        self._playback_thread.start()

    def _open_output_stream(self) -> None:
        """Create audio output sink for bytes from media file"""

        output_sink = self._p.open(
            format=pyaudio.paInt16,
            channels=self.media_info["channels"],
            rate=self.media_info["sample_rate"],
            output=True,
        )

        self._output = OutputStream(output_sink)


class InputStream:
    """Wrapper for ffmpeg transcoding process"""

    def __init__(self, process: Popen[bytes]) -> None:
        self.process = process

    def read(self, n: int = -1) -> bytes:
        if self.process.stdout is None:
            return bytes(0)

        return self.process.stdout.read(n)


class OutputStream:
    """Wrapper for PyAudio output sink"""

    def __init__(self, sink: PyAudioStream) -> None:
        self.sink = sink

    def write(self, frames: bytes) -> None:
        self.sink.write(frames)


def system_time() -> int:
    return int(t.time() * MILLISECONDS)


def clamp(value: int, min_value: int, max_value: int) -> int:
    return min(max(min_value, value), max_value)
