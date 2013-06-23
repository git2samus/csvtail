#!/usr/bin/env python
import sys, csv
from curses import wrapper

class GenRows(object):
    def __init__(self, f):
        self._rowpos = 0
        self._rowlen = 0
        self._rowiter = self._rowgen(f)
        self.rowindex = []

    def _linegen(self, f):
        """ auxiliary generator to return lines for csv.reader while tracking line length """
        for line in f:
            self._rowlen += len(line)
            yield line

    def _rowgen(self, f):
        """ yield csv rows from file while updating rowpos index """
        for row in csv.reader(self._linegen(f)):
            self.rowindex.append(self._rowpos)
            yield row
            self._rowpos += self._rowlen
            self._rowlen = 0

    def __iter__(self):
        return self

    def next(self):
        return self._rowiter.next()

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
        while True:
            try:
                print genrows.next()
            except StopIteration:
                break
        print genrows.rowindex

