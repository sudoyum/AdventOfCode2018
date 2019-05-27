#!/usr/bin/env python3

import os
import re
import sys

import numpy as np


# TODO: Data structure without class
class MovingPoint(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy


class Plane(object):
    MAX_WIDTH = 100000
    MAX_LENGTH = 100000

    def __init__(self, p_list, width=MAX_WIDTH, length=MAX_LENGTH):
        self.width = width
        self.length = length
        self.plane = np.zeros((self.width, self.length), dtype=np.int8)
        self.mp = p_list
        for p in p_list:
            self.plane[p.x, p.y] = 1
        self.seconds = 0

    def print_plane(self):
        max_x = max(self.mp, key=lambda item: item.x)
        max_y = max(self.mp, key=lambda item: item.y)

        min_x = min(self.mp, key=lambda item: item.x)
        min_y = min(self.mp, key=lambda item: item.y)
        for i in range(min_x.x-1, max_x.x+1):
            for j in range(min_y.y, max_y.y+1):
                if self.plane[i, j] > 0:
                    sys.stdout.write("#")
                else:
                    sys.stdout.write(".")
            sys.stdout.write("\n")

    def rect_area(self):
        max_x = max(self.mp, key=lambda item: item.x)
        max_y = max(self.mp, key=lambda item: item.y)

        min_x = min(self.mp, key=lambda item: item.x)
        min_y = min(self.mp, key=lambda item: item.y)

        return (max_x.x - min_x.x)*(max_y.y-min_y.y)

    def update_plane(self):
        self.seconds += 1
        for p in self.mp:
            self.plane[p.x, p.y] -= 1
            p.update()
            self.plane[p.x, p.y] += 1


def solve_p1_p2(point_list):
    if __debug__:
        plane = Plane(point_list, 20, 20)
        min_area = plane.rect_area()
        while True:
            plane.update_plane()
            new_area = plane.rect_area()
            if new_area < min_area:
                min_area = new_area
            else:
                print("area=%d" % min_area)
            if new_area == 63:
                plane.print_plane()
                sys.exit(1)
    else:
        plane = Plane(point_list)
        min_area = plane.rect_area()
        while True:
            plane.update_plane()
            new_area = plane.rect_area()
            if new_area < min_area:
                min_area = new_area
            else:
                print("area=%d" % min_area)
            if new_area == 549:
                plane.print_plane()
                print("PART2:%d" % plane.seconds)
                sys.exit(1)

    print("PART1: %d")


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    point_list = []
    for entry in data_list:
        match = re.search(r"position\=<([\d\s-]+),([\d\s-]+)\> velocity\=<([\d\s-]+),([\d\s-]+)", entry).groups()
        if match:
            point_list.append(MovingPoint(int(match[0]), int(match[1]), int(match[2]), int(match[3])))
    solve_p1_p2(point_list)


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


