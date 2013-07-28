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
    def format_field(csv_field_i, csv_field):
        #TODO color \n replacements
        field = csv_field.replace("\n", u"\u23CE")  # 'RETURN SYMBOL' (U+23CE)
        colwidth = csv_colwidths[csv_field_i + csv_col_offset]

        result = '{{field:>{colwidth}}}'
        result = result.format(colwidth=colwidth)
        result = result.format(field=field)

        return result

    def update_scr():
        stdscr.clear()  # clear screen and mark for refresh

        # rows from CSV that are visible
        row_slice = slice(csv_row_offset, csv_row_offset + num_scr_rows)
        for scr_row_i, csv_row in enumerate(csv_rows[row_slice]):
            # pad each visible field to optimum width and create grid
            rowtext = (
                format_field(csv_field_i, csv_field)
                for csv_field_i, csv_field
                in enumerate(csv_row[csv_col_offset:])
            )
            rowtext = '|'.join(rowtext)
            rowtext = '|{}|'.format(rowtext)

            # draw a line (no longer than the terminal's width)
            stdscr.addnstr(scr_row_i, 0, rowtext, num_scr_cols)

    # total rows
    num_csv_rows = len(csv_rows)

    # calculate maximum width of each column
    csv_colwidths = []
    for csv_row in csv_rows:
        for csv_field_i, csv_field in enumerate(csv_row):
            if len(csv_colwidths) <= csv_field_i:
                csv_colwidths.append(0)
            csv_colwidths[csv_field_i] = max(
                csv_colwidths[csv_field_i], len(csv_field)
            )

    # get (current) screen dimensions
    num_scr_rows, num_scr_cols = stdscr.getmaxyx()

    # row and col from which the CSV should start printing
    csv_row_offset, csv_col_offset = 0, 0

    # keys we'll respond to, grouped by action
    #TODO ESC has delay for escape sequences
    action_keys = {
        'quit':   set((ord('q'),)),
        'resize': set((curses.KEY_RESIZE,)),
        'up':     set((ord('k'), curses.KEY_UP,)),
        'down':   set((ord('j'), curses.KEY_DOWN,)),
        'left':   set((ord('h'), curses.KEY_LEFT,)),
        'right':  set((ord('l'), curses.KEY_RIGHT,)),
    }
    movement_keys = set(
        key
        for action in ('up', 'down', 'left', 'right')
        for key in action_keys[action]
    )

    # additional properties
    curses.curs_set(0)

    # paint initial screen
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
