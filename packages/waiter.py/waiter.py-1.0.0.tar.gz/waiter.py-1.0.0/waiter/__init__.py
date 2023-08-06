from time import sleep
from typing import Callable
from functools import partial

from datetime import datetime, timedelta

__WAITS: dict[float, tuple[datetime, float]] = {}


def create_waiter(duration: float, *, overwrite_existing=False) -> Callable[[], None]:
    if duration not in __WAITS or overwrite_existing:
        __WAITS[duration] = (datetime.now() + timedelta(milliseconds=duration), duration)

    return partial(__try_wait, duration)


def __try_wait(key: float) -> None:
    now = datetime.now()
    (limited_until, duration) = __WAITS[key]
    sleep_duration = (limited_until - now).total_seconds()
    if now < limited_until:
        sleep(sleep_duration)

    __WAITS[key] = (datetime.now() + timedelta(milliseconds=duration), duration)
