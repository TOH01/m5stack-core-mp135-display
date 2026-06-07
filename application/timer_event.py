import time
from typing import Callable


class TimerEvent:
    def __init__(self, interval_ms: int, callback: Callable) -> None:
        self.interval_ms = interval_ms
        self.callback = callback
        self.last_time_ms = time.monotonic_ns() // 1_000_000

    def reset(self) -> None:
        self.last_time_ms = time.monotonic_ns() // 1_000_000

    def check(self) -> None:
        current_time_ms = time.monotonic_ns() // 1_000_000

        if current_time_ms - self.last_time_ms >= self.interval_ms:
            self.callback()
            self.last_time_ms = current_time_ms
