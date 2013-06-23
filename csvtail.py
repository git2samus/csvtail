#!/usr/bin/env python
import sys, csv
from curses import wrapper

class GenRows(object):
    def __init__(self, f):
        self.f = f
        self.rowindex = []
        self._rowpos = 0
        self._rowlen = 0

    @property
    def rowpos(self):
        return self._rowpos

    def _linegen(self):
        """ auxiliary generator to return lines for csv.reader while tracking line length """
        for line in self.f:
            self._rowlen += len(line)
            yield line

    def __iter__(self):
        """ yield csv rows from file while updating rowpos index """
        for row in csv.reader(self._linegen()):
            self.rowindex.append(self._rowpos)
            yield row
            self._rowpos += self._rowlen
            self._rowlen = 0


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
        genrows = GenRows(f)
        for row in genrows:
            print genrows.rowpos, row
        print genrows.rowindex

