#!/usr/bin/env python
import sys, csv
from curses import wrapper

# globals to modify from generators without affecting yield signature
rowpos, rowlen = 0, 0

def genrows(f):
    """ yield csv rows from file while updating rowpos index """
    def linegen():
        """ auxiliary generator to return lines for csv.reader while tracking line length """
        global rowlen
        for line in f:
            rowlen += len(line)
            yield line

    global rowpos, rowlen
    for row in csv.reader(linegen()):
        yield row
        rowpos += rowlen
        rowlen = 0


'''
def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 10):
        v = i - 10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10 / v))

    stdscr.refresh()
    stdscr.getkey()
'''


if __name__ == '__main__':
    #wrapper(main)
    with open(sys.argv[1]) as f:
        for row in genrows(f):
            print rowpos, row

