#!/usr/bin/env python3

import os
import re
import sys

import numpy as np


#. =0, # =1, | =2, ~ = 3
BARE = 0
CLAY = 1
PASSED = 2
WATER = 3
class Clay(object):
    def __init__(self, max_x, min_x, max_y, min_y, clay):
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y
        self.spring = (500, 0)
        if __debug__:
             print("max_x = %d, max_y = %d" % (max_x, max_y))
             print("min_x = %d, min_y = %d" % (min_x, min_y))
        self.plane = np.zeros((max_x + 2, max_y + 2), dtype=np.int8)
        for c in clay:
            self.plane[c] = 1
        self.index = 0
        self.trickle_points = []
        self.blacklist = []

    def debug_print(self):
        for j in range(self.min_y, self.max_y + 1):
            for i in range(self.min_x-1, self.max_x + 2):
                if self.plane[(i, j)] == 0:
                    sys.stdout.write('.')
                elif self.plane[(i, j)] == 1:
                    sys.stdout.write('#')
                elif self.plane[(i, j)] == 2:
                    sys.stdout.write('|')
                elif self.plane[(i, j)] == 3:
                    sys.stdout.write('~')
            sys.stdout.write('%d\n' % j)

    def count_water_passed(self):
        count = 0
        for i in range(0, self.max_x+2):
            for j in range(self.min_y, self.max_y+1):
                if self.plane[(i, j)] > 1:
                    count += 1
        return count

    def count_water(self):
        count = 0
        for i in range(0, self.max_x+2):
            for j in range(self.min_y, self.max_y+1):
                if self.plane[(i, j)] == WATER:
                    count += 1
        return count

    def trickle(self):
        trickle = self.spring
        x, y = trickle
        while True:
            if self.plane[trickle] == CLAY or self.plane[trickle] == WATER:
                y -= 1
                decision_point = (x, y)
                points = []
                spill_l = False
                spill_r = False
                while self.plane[(x + 1, y)] != CLAY and (
                        (self.plane[(x + 1, y + 1)] == CLAY) or (self.plane[(x + 1, y + 1)] == WATER)):
                    x += 1
                    points.append((x, y))
                    self.plane[(x, y)] = 2
                    #print("BARR=(%d, %d)" % (x, y))
                if self.plane[(x + 1, y + 1)] != CLAY and self.plane[(x + 1, y + 1)] != WATER:
                    if (x+1, y) not in self.blacklist:
                        self.trickle_points.append((x + 1, y))
                        self.blacklist.append((x+1, y))
                    spill_r = True

                x = decision_point[0]
                while self.plane[(x - 1, y)] != CLAY and (
                        (self.plane[(x - 1, y + 1)] == CLAY) or (self.plane[(x - 1, y + 1)] == WATER)):
                    x -= 1
                    points.append((x, y))
                    self.plane[(x, y)] = 2
                    #print("BARL=(%d, %d)" % (x, y))

                if self.plane[(x - 1, y + 1)] != CLAY and self.plane[(x - 1, y + 1)] != WATER:
                    if (x-1, y) not in self.blacklist:
                        self.trickle_points.append((x - 1, y))
                        self.blacklist.append((x-1, y))
                    spill_l = True
                if len(self.trickle_points) == 0 or (len(self.trickle_points) != 0 and (not spill_l and not spill_r)):
                    for point in points:
                        self.plane[point] = WATER
                        #print("WATER=(%d, %d)" % (point[0], point[1]))
                    self.plane[decision_point] = WATER
                    #print("WATER=(%d, %d)" % (decision_point[0], decision_point[1]))
                    trickle = (decision_point[0], decision_point[1])
                    x, y = trickle
                else:
                    self.plane[decision_point] = 2
                    trickle = self.trickle_points.pop(0)
                    x, y = trickle

            else:
                self.plane[(x, y)] = 2
                #print("BARD=(%d, %d)" % (x, y))
                y += 1
                trickle = (x, y)
                if y > self.max_y:
                    if len(self.trickle_points) == 0:
                        #self.debug_print()
                        return
                    else:
                        trickle = self.trickle_points.pop(0)
                        #print("TRICKLE POINT=(%d, %d)" % (trickle[0], trickle[1]))
                        x, y = trickle


def solve_p1(max_x, min_x, max_y, min_y, clay):
    clay = Clay(max_x, min_x, max_y, min_y, clay)
    clay.trickle()
    print("PART1: %d" % clay.count_water_passed())


def solve_p2(max_x, min_x, max_y, min_y, clay):
    clay = Clay(max_x, min_x, max_y, min_y, clay)
    clay.trickle()
    print("PART2: %d" % clay.count_water())


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    clay = []
    max_x = 0
    min_x = 1e10
    max_y = 0
    min_y = 1e10
    for data in data_list:
        match = re.search(r"([xy])=(\d+), ([xy])=(\d+)..(\d+)", data)
        if match:
            if int(match.group(2)) > max_x and match.group(1) == 'x':
                max_x = int(match.group(2))
            if int(match.group(5)) > max_x and match.group(3) == 'x':
                max_x = int(match.group(5))
            if int(match.group(2)) > max_y and match.group(1) == 'y':
                max_y = int(match.group(2))
            if int(match.group(5)) > max_y and match.group(3) == 'y':
                max_y = int(match.group(5))
            if int(match.group(2)) < min_y and match.group(1) == 'y':
                min_y = int(match.group(2))
            if int(match.group(4)) < min_y and match.group(3) == 'y':
                min_y = int(match.group(4))
            if int(match.group(2)) < min_x and match.group(1) == 'x':
                min_x = int(match.group(2))
            if int(match.group(4)) < min_x and match.group(3) == 'x':
                min_x = int(match.group(4))
            clay_points = []
            if match.group(1) == 'x':
                x = int(match.group(2))
                for y in range(int(match.group(4)), int(match.group(5)) + 1):
                    clay_points.append((x, y))
                clay += clay_points
            if match.group(1) == 'y':
                y = int(match.group(2))
                for x in range(int(match.group(4)), int(match.group(5)) + 1):
                    clay_points.append((x, y))
                clay += clay_points

    solve_p1(max_x, min_x, max_y, min_y, clay)
    solve_p2(max_x, min_x, max_y, min_y, clay)


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


