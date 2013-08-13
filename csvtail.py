#!/usr/bin/env python3
import sys
from decorator import with_curses
from ui.interface import Interface


@with_curses
def run_interface(stdscr, *csv_fnames):
    interface = Interface(*csv_fnames)
    interface.run(stdscr)


if __name__ == '__main__':
    #TODO help/usage
    #TODO commandline args
    #TODO error messages
    csv_fnames = sys.argv[1:]
    run_interface(*csv_fnames)
