#!/usr/bin/env python3
import curses
from functools import wraps


def with_curses(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return curses.wrapper(f, *args, **kwargs)
    return wrapper


@with_curses
def main(stdscr):
    while True:
        key = stdscr.getkey()
        stdscr.clear()
        stdscr.addstr(0, 0, '{}x{}'.format(curses.LINES, curses.COLS))
        stdscr.addstr(1, 0, '{}'.format(stdscr.getmaxyx()))
        stdscr.addstr(2, 0, '{}'.format(key))
        stdscr.refresh()


if __name__ == '__main__':
    main()
