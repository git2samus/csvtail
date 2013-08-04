#!/usr/bin/env python3
import sys
from ui import interface
from models import CSV


if __name__ == '__main__':
    #TODO help/usage
    #TODO commandline args
    #TODO error messages
    csv_fnames = sys.argv[1:]
    csv_models = (CSV(fname) for fname in csv_fnames)

    # start curses
    interface(*csv_models)
