#!/usr/bin/env python3

import os
import re
import sys

import numpy as np


class Cave(object):
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.plane = np.zeros((self.depth, self.depth), dtype=np.int8)
        self.geologic = np.zeros((self.depth, self.depth), dtype=np.int64)
        self.erosion = np.zeros((self.depth, self.depth), dtype=np.int64)
        self.mouth = (0, 0)
        self.fewest_steps = 0

    def debug_print(self):
        for j in range(0, self.target[1] + 5):
            for i in range(0, self.target[0] + 5):
                if i == 0 and j == 0:
                    sys.stdout.write('M')
                elif i == self.target[0] and j == self.target[1]:
                    sys.stdout.write('T')
                else:
                    region = self.erosion[(i, j)] % 3
                    if region == 0:
                        sys.stdout.write('.')
                    elif region == 1:
                        sys.stdout.write('=')
                    elif region == 2:
                        sys.stdout.write('|')
            sys.stdout.write('\n')

    def set_features(self):
        self.geologic[(0, 0)] = 0
        self.erosion[(0, 0)] = self.depth % 20183
        for i in range(1, self.depth):
            self.geologic[(i, 0)] = i * 16807
            self.erosion[(i, 0)] =(self.geologic[(i, 0)] + self.depth) % 20183
        for j in range(1, self.depth):
            self.geologic[(0, j)] = j * 48271
            self.erosion[(0, j)] = (self.geologic[(0, j)] + self.depth) % 20183
        self.geologic[(self.target[0], self.target[1])] = 0
        self.erosion[(self.target[0], self.target[1])] = self.depth % 20183
        for j in range(1, self.depth):
            for i in range(1, self.depth):
                if not(j == self.target[1] and i == self.target[0]):
                    self.geologic[(i, j)] = self.erosion[(i - 1, j)] * self.erosion[(i, j - 1)]
                    self.erosion[(i, j)] = (self.geologic[(i, j)] + self.depth) % 20183

        for i in range(self.mouth[0], self.target[0] + 1):
            for j in range(self.mouth[1], self.target[1] + 1):
                self.plane[(i, j)] = self.erosion[(i, j)] % 3

    def count_risk(self):
        return np.sum(self.plane[self.mouth[0]:self.target[0] + 1, self.mouth[1]:self.target[1] + 1])

    def traverse(self):
        print("TODO:")


def solve_p1(depth, target):
    cave = Cave(depth, target)
    cave.set_features()
    #cave.debug_print()
    print("PART1: %d" % (cave.count_risk()))


def solve_p2(depth, target):
    cave = Cave(depth, target)
    cave.set_features()
    cave.traverse()
    print("PART2: %d" % cave.fewest_steps)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    match = re.search(r"depth: (\d+)", data_list[0])
    if match:
        depth = int(match.group(1))
    else:
        print("input issue")
        sys.exit(1)
    match = re.search(r"target: (\d+),(\d+)", data_list[1])
    if match:
        target = (int(match.group(1)), int(match.group(2)))
    else:
        print("input issue")
        sys.exit(1)

    solve_p1(depth, target)
    #solve_p2(depth, target)


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
