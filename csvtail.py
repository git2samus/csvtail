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
    def update_scr():
        stdscr.clear()
        stdscr.addstr(0, 0, '{}-{} ({}x{})'.format(
            csv_row_offset, csv_col_offset,
            num_scr_rows, num_scr_cols,
        ))

    # total rows
    num_csv_rows = len(csv_rows)
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
    csv_row_offset, csv_col_offset = 0, 0

    # keys we'll respond to, grouped by action
    #TODO ESC has delay for escape sequences
    action_keys = {
        'quit':   (ord('q'),),
        'resize': (curses.KEY_RESIZE,),
        'up':     (ord('k'), curses.KEY_UP,),
        'down':   (ord('j'), curses.KEY_DOWN,),
        'left':   (ord('h'), curses.KEY_LEFT,),
        'right':  (ord('l'), curses.KEY_RIGHT,),
    }
    movement_keys = set(
        key
        for action in ('up', 'down', 'left', 'right')
        for key in action_keys[action]
    )

    # initial screen
    update_scr()

    # main loop
    while True:
        key = stdscr.getch()  # this calls stdscr.refresh()

        if key in action_keys['quit']:
            break  # exit main loop
        elif key in action_keys['resize']:
            # update screen dimensions
            num_scr_rows, num_scr_cols = stdscr.getmaxyx()
            # mark screen for redraw to avoid clipping issues
            curses.doupdate()
        elif key in movement_keys:
            #TODO else offset (curses.flash/curses.beep?)
            if key in action_keys['up']:
                if csv_row_offset > 0:
                    csv_row_offset -= 1
            elif key in action_keys['down']:
                if csv_row_offset < num_csv_rows - 1:
                    csv_row_offset += 1
            elif key in action_keys['left']:
                if csv_col_offset > 0:
                    csv_col_offset -= 1
            elif key in action_keys['right']:
                if csv_col_offset < len(csv_colwidths) - 1:
                    csv_col_offset += 1

            # update screen buffer
            update_scr()


if __name__ == '__main__':
    # load entire CSV in memory
    #TODO get csv.reader arguments from sys.argv
    #TODO work around stdin to read files and keys
    fname = sys.argv[1]
    with open(fname) as fobj:
        csv_rows = tuple(csv.reader(fobj))

    # start curses
    main(csv_rows)
