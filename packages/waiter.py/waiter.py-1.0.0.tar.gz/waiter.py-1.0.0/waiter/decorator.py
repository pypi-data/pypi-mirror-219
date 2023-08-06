from functools import wraps

from . import create_waiter


def will_wait(duration: float):
    wait = create_waiter(duration)

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            wait()
            return result

        return wrapper

    return inner
