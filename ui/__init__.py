import curses
from functools import wraps
from ui.view import View


def with_curses(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return curses.wrapper(func, *args, **kwargs)

    # return wrapped function
    return wrapper


@with_curses
def interface(stdscr, *csv_models):
    views = [View(csv_model) for csv_model in csv_models]
    return views
