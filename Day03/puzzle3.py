#!/usr/bin/env python3

import os
import sys
import re

import numpy as np


#numpy in pycharm debugger "View as Array" option is cool
#numpy is slower than list?
class Fabric(object):
    def __init__(self, id, x, y, length, width):
        self.id = id
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.has_overlap = False

    def contains_point(self, point):
        if self.x <= point[0] <= self.x + self.width:
            if self.y <= point[1] <= self.y + self.length:
                return True
        return False


def solve_p1(entry_list):
    fabric_longest = max(entry_list, key=lambda item: item.length + item.y)
    fabric_widest = max(entry_list, key=lambda item: item.width + item.x)
    max_len = fabric_longest.length + fabric_longest.y
    max_width = fabric_widest.width + fabric_widest.x
    if __debug__:
        print("max_len=%d" % max_len)
        print("max_width=%d" % max_width)
    plane = np.zeros((max_width, max_len), dtype=np.int32)
    for fabric in entry_list:
        for i in range(0, fabric.width):
            for j in range(0, fabric.length):
                plane[fabric.x + i, fabric.y + j] += 1
    overlap = (plane > 1).sum()
    print("PART1: %d" % overlap)


def solve_p2(entry_list):
    fabric_longest = max(entry_list, key=lambda item: item.length + item.y)
    fabric_widest = max(entry_list, key=lambda item: item.width + item.x)
    max_len = fabric_longest.length + fabric_longest.y
    max_width = fabric_widest.width + fabric_widest.x
    if __debug__:
        print("max_len=%d" % max_len)
        print("max_width=%d" % max_width)
    plane = np.zeros((max_width, max_len), dtype=np.int32)
    overlap_points = []
    for fabric in entry_list:
        for i in range(0, fabric.width):
            for j in range(0, fabric.length):
                plane[fabric.x + i, fabric.y + j] += 1
                if plane[fabric.x + i, fabric.y + j] > 1:
                    overlap_points.append((fabric.x + i, fabric.y + j))
    for fabric in entry_list:
        count = 0
        for point in overlap_points:
            if fabric.contains_point(point):
                count += 1
                break
        if count == 0:
            print("PART2: %s" % fabric.id)
            sys.exit(1)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    entry_list = []
    for entry in data_list:
        match = re.search(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)", entry)
        if match:
            id = match.group(1)
            x = int(match.group(2))
            y = int(match.group(3))
            width = int(match.group(4))
            length = int(match.group(5))
            fabric_piece = Fabric(id, x, y, length, width)
            entry_list.append(fabric_piece)
        else:
            print("Issue with regex/input")
            sys.exit(1)

    solve_p1(entry_list)
    solve_p2(entry_list)


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
