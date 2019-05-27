#!/usr/bin/env python3

import os
import sys

from collections import defaultdict

def manhattan_dist(point1, point2):
    dist = 0
    for i in range(0, 4):
        dist += abs(point2[i] - point1[i])
    return dist


def print_constellation(constellations):
    for k, v in constellations.items():
        print(k, v)
    print("NUM CONSTELLATIONS: %d" % len(constellations))


def solve_p1(points):
    constellations = defaultdict(list)
    for i in range(0, len(points)):
        none_added = True
        for j in range(0, len(points)):
            if j != i:
                dist = manhattan_dist(points[i], points[j])
                if dist <= 3:
                    constellations[i].append(j)
                    none_added = False
        if none_added:
            constellations[i] = []

    constellations_filt = defaultdict(list)
    visited = set()
    for k, v in constellations.items():
        if k not in visited:
            visited.add(k)
            stars = v
            while True:
                new_v = []
                for star in stars:
                    for val in constellations[star]:
                        if val not in stars:
                            new_v.append(val)
                        visited.add(val)

                if len(new_v) == 0:
                    break
                else:
                    for new in set(new_v):
                        stars.append(new)
            constellations_filt[k] = stars
        if len(v) == 0:
            constellations_filt[k] = k
    print("PART1: %d" % len(constellations))


def solve_p2():
    print("PART2: %d")


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    points = []
    for data in data_list:
        (i, j, k, l) = data.split(',')
        points.append((int(i), int(j), int(k), int(l)))
    solve_p1(points)
    #solve_p2()


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


