import curses
from functools import wraps


def with_curses(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return curses.wrapper(func, *args, **kwargs)

    # return wrapped function
    return wrapper
