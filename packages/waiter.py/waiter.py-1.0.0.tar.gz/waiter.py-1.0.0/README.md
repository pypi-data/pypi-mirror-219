# waiter.py

[![PyPI](https://img.shields.io/pypi/v/waiter.py?color=0073b7&label=version&logo=python&logoColor=white&style=flat-square) ![PyPI - Downloads](https://img.shields.io/pypi/dd/waiter.py?color=0073b7&logo=python&logoColor=white&style=flat-square)](https://pypi.org/project/waiter.py/)

A more efficient way of conforming to limits via waiting

---

Think of _waiter_ as Python's built-in `sleep()` function but instead of sleeping every time it is called, it will only sleep if it **needs** to. This makes it easier to conform to known rate limits while avoiding unnecessary sleeps.

Let's assume you are consuming a REST API that has a rate limit of 2 requests per second. Naturally you could simply sleep for 500ms after each request as to not hit this limit. However what if you make one request, sleep for 500ms, do something else that takes longer than 500ms, make another request, and then sleep once more for 500ms? The last sleep would be unnecessary.

_waiter_ lets you create functions that will only sleep when needed:

```python
from waiter import create_waiter

wait = create_waiter(500)

make_quick_request()  # takes 10ms
wait()  # sleeps for 490ms
make_slow_request()  # takes 1000ms
wait()  # does not sleep
```

You can also decorate functions:

```python
from waiter.decorator import will_wait

@will_wait(500)
def my_func():
    #  ...

#  You know the drill
```
