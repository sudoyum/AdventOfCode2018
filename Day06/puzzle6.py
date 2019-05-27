#!/usr/bin/env python3

import os
import re
import sys

from collections import defaultdict
import numpy as np


class Point(object):
    def __init__(self, x, y, id_num):
        self.x = x
        self.y = y
        self.id_num = id_num
        self.manhattan = 0
        self.on_edge = False
        self.total_dist = 0

    def set_total_dist(self, dist):
        self.total_dist = dist

    def distance(self, c, d):
        return abs(self.x - c) + abs(self.y - d)


class PointPlane(object):
    def __init__(self, points):
        self.points = points
        self.max_x = max(points, key=lambda c: c.x).x
        self.max_y = max(points, key=lambda c: c.y).y
        self.plane = np.zeros((self.max_x + 1, self.max_y + 1), dtype=np.int16)
        self.on_edge = None

    def determine_dists(self):
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                dists = {}
                for point in self.points:
                    dists[point.id_num] = point.distance(x, y)
                if len([x for x in dists.values() if x == min(dists.values())]) == 1:
                    self.plane[(x, y)] = min(dists, key=dists.get)

    def determine_total_dists(self):
        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                for point in self.points:
                    self.plane[(x, y)] += point.distance(x, y)

    def determine_on_edge(self):
        on_edge = []
        for y in range(0, self.max_y + 1):
            on_edge.append(self.plane[(0, y)])
        for x in range(0, self.max_x + 1):
            on_edge.append(self.plane[(x, 0)])
        for y in range(0, self.max_y + 1):
            on_edge.append(self.plane[(self.max_x, y)])
        for x in range(0, self.max_x + 1):
            on_edge.append(self.plane[(x, self.max_y)])
        self.on_edge = set(on_edge)

    def largest_non_edge(self):
        areas = defaultdict(int)
        for x in range(0, self.max_x + 1):
            for y in range(0, self.max_y + 1):
                if self.plane[(x, y)] not in self.on_edge:
                    areas[self.plane[(x, y)]] += 1
        return max(areas.values())

    def total_lt1k(self):
        total_size = 0
        for x in range(0, self.max_x + 1):
            for y in range(0, self.max_y + 1):
                if self.plane[(x, y)] < 10000:
                    total_size += 1
        return total_size


def solve_p1(points):
    pp = PointPlane(points)
    pp.determine_dists()
    pp.determine_on_edge()
    print("PART1: %d" % pp.largest_non_edge())


def solve_p2(points):
    pp = PointPlane(points)
    pp.determine_total_dists()
    print("PART2: %d" % pp.total_lt1k())


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    points = []
    id_num = 1
    for line in data_list:
        m = re.search(r"(\d+), (\d+)", line.strip('\n'))
        if m:
            points.append(Point(int(m.group(1)), int(m.group(2)), id_num))
            id_num += 1
    solve_p1(points)
    solve_p2(points)


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
