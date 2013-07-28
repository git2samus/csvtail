#!/usr/bin/env python3
import sys
import csv
import curses
from functools import wraps


def with_curses(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return curses.wrapper(func, *args, **kwargs)
    return wrapper


@with_curses
def main(stdscr, csv_rows):
    def update_src():
        stdscr.clear()
        for scr_row_i in range(num_scr_rows):
            stdscr.addstr(scr_row_i, 0, '{}'.format(scr_row_i))

    # total rows
    #num_csv_rows = len(csv_rows)
    # calculate maximum width of each column
    csv_colwidths = []
    for csv_row in csv_rows:
        for csv_cell_i, csv_cell in enumerate(csv_row):
            if len(csv_colwidths) <= csv_cell_i:
                csv_colwidths.append(0)
            csv_colwidths[csv_cell_i] = max(
                csv_colwidths[csv_cell_i], len(csv_cell)
            )

    # get (current) screen dimensions
    num_scr_rows, num_scr_cols = stdscr.getmaxyx()
    # row and col from which the CSV should start printing
    #csv_offset_row, csv_offset_col = 0, 0

    # keys we'll respond to, grouped by action
    action_keys = {
        'quit':   ('q',),
        'resize': ('KEY_RESIZE',),
    }

    # main loop
    while True:
        update_src()

        key = stdscr.getkey()
        if key in action_keys['quit']:
            break

        if key in action_keys['resize']:
            # update screen dimensions
            num_scr_rows, num_scr_cols = stdscr.getmaxyx()


if __name__ == '__main__':
    # load entire CSV in memory
    #TODO get csv.reader arguments from sys.argv
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        with open(fname) as fobj:
            csv_rows = tuple(csv.reader(fobj))
    else:
        csv_rows = tuple(csv.reader(sys.stdin))

    # start curses
    main(csv_rows)
