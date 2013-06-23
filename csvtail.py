#!/usr/bin/env python
import sys, csv
from curses import wrapper

class GenRows(object):
    def __init__(self, f):
        self.f = f
        self.rowpos = 0
        self.rowlen = 0

    def __iter__(self):
        """ yield csv rows from file while updating rowpos index """
        def linegen():
            """ auxiliary generator to return lines for csv.reader while tracking line length """
            for line in self.f:
                self.rowlen += len(line)
                yield line

        for row in csv.reader(linegen()):
            yield row
            self.rowpos += self.rowlen
            self.rowlen = 0


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

