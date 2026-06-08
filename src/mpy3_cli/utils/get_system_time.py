import time

from mpy3_cli.utils.constants import MILLISECONDS


def get_system_time() -> int:
    return int(time.time() * MILLISECONDS)
