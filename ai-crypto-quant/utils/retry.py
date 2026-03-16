from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry(func: Callable[[], T], times: int = 3, wait: float = 0.5) -> T:
    last_exc: Exception | None = None
    for _ in range(times):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(wait)
    if last_exc:
        raise last_exc
    raise RuntimeError("retry failed without exception")
