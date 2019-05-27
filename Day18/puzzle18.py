#!/usr/bin/env python3

import os
import sys


import numpy as np

DIM = 50


class Lumber(object):
    def __init__(self, plot):
        self.plot = plot
        self.plot_next = self.plot.copy()
        self.sets = set()
        self.minute = 0

    def debug_print(self):
        for i in range(DIM):
            for j in range(DIM):
                if self.plot[(i, j)] == 1:
                    sys.stdout.write('|')
                elif self.plot[(i, j)] == 2:
                    sys.stdout.write('#')
                else:
                    sys.stdout.write('.')
            sys.stdout.write('\n')

    def get_total_resources(self):
        wooded = 0
        yards = 0
        for i in range(DIM):
            for j in range(DIM):
                if self.plot[(i, j)] == 1:
                    wooded += 1
                elif self.plot[(i, j)] == 2:
                    yards += 1
        return wooded * yards

    def _get_adjacent(self, i, j):
        adjacent = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if ((x + i) < DIM) and ((y + j) < DIM) and\
                   ((x + i) >= 0) and ((y + j) >= 0):
                    if not (x == 0 and y == 0):
                        adjacent.append(self.plot[(x+i, y+j)])
        return adjacent

    def do_minute(self):
        self.minute += 1
        for i in range(DIM):
            for j in range(DIM):
                if self.plot[(i, j)] == 0:
                    adjacent = self._get_adjacent(i, j)
                    if adjacent.count(1) >= 3:
                        self.plot_next[i, j] = 1
                elif self.plot[(i, j)] == 1:
                    adjacent = self._get_adjacent(i, j)
                    if adjacent.count(2) >= 3:
                        self.plot_next[i, j] = 2
                elif self.plot[(i, j)] == 2:
                    adjacent = self._get_adjacent(i, j)
                    if (adjacent.count(2) > 0) and\
                       (adjacent.count(1) > 0):
                        self.plot_next[(i, j)] = 2
                    else:
                        self.plot_next[(i, j)] = 0
        self.plot = self.plot_next.copy()


def solve_p1(plot):
    lumber = Lumber(plot)
    for i in range(10):
        lumber.do_minute()
        #lumber.debug_print()
    print("PART1: %d" % lumber.get_total_resources())


def solve_p2(plot):
    lumber = Lumber(plot)
    #minute 452 starts cycle of v=173922
    for i in range(452):
        lumber.do_minute()

    #(1000000000-452) % 28 repeats every 28
    for i in range(16):
        lumber.do_minute()

    print("PART2: %d" % lumber.get_total_resources())


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    plot = np.zeros((DIM, DIM), dtype=np.int8)
    for i in range(0, len(data_list)):
        for j in range(0, len(data_list[i])):
            if data_list[i][j] == '|':
                plot[(i, j)] = 1
            if data_list[i][j] == '#':
                plot[(i, j)] = 2
    solve_p1(plot)
    solve_p2(plot)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./<prog.py> <input_file>")
        if __debug__:
            print(sys.argv)
        sys.exit(1)
    else:
        f_name = sys.argv[1]
        if __debug__:
            print("Passed in filename=%s" % f_name)
        if not os.path.exists(f_name):
            print("Can't locate input file")
            sys.exit(1)
        else:
            format_input(f_name)
