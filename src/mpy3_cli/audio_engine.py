from pathlib import Path
from subprocess import Popen
from threading import Thread

import pyaudio  # type: ignore
from pyaudio import PyAudio  # type: ignore
from pyaudio import Stream as PyAudioStream  # type: ignore

from mpy3_cli import ffapi
from mpy3_cli.types import MediaInfo
from mpy3_cli.utils.noalsaerr import noalsaerr

CHUNK_SIZE = 1024

DEFAULT_FORMAT = "s16le"
DEFAULT_CODEC = "pcm_s16le"
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 2


class AudioEngine:
    """Handles media playback"""

    def __init__(self, mrl: Path) -> None:
        self.mrl = mrl

        self._input: InputStream | None = None
        self._output: OutputStream | None = None
        self._playback_thread: Thread | None = None

        with noalsaerr():
            self._p: PyAudio = PyAudio()

        self.media_info: MediaInfo = ffapi.probe_media(self.mrl)

        self.format = DEFAULT_FORMAT
        self.codec = DEFAULT_CODEC

    def play(self) -> None:
        self._open_input_stream()

    def _playback(self) -> None:
        if self._input is None:
            raise ValueError('"self._input" has not been set.')

        if self._output is None:
            raise ValueError('"self._output" has not been set.')

        print(f"Playing {self.mrl}")

        while True:
            data = self._input.read(CHUNK_SIZE)
            if not data:
                print("Playback complete")
                break

            self._output.write(data)

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
