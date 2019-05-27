#!/usr/bin/env python3

import os
import sys

import numpy as np


# TODO: Part2 takes 118 seconds, mostly in 'reduce' of 'numpy.ufunc'
def pwr_level(x, y, serial_num):
    rack_id = x + 10
    pwr_lvl = rack_id * y
    pwr_lvl += serial_num
    pwr_lvl *= rack_id
    pwr_lvl = (pwr_lvl // 100) % 10
    pwr_lvl -= 5
    return pwr_lvl


class FuelDevice(object):
    def __init__(self, serial_num):
        self.three_by_three = {}
        self.plane_val = np.empty((300, 300), dtype=np.int32)

        for i in range(300):
            for j in range(300):
                self.plane_val[i, j] = pwr_level(i, j, serial_num)

    def print_cell(self, coord):
        print("power at cell (%d,%d) = %d" % (coord[0], coord[1], self.plane_val[coord]))

    def sum_three(self):
        start_point = {}
        for i in range(300-3):
            for j in range(300-3):
                sum = 0
                for x in range(i, i+3):
                    for y in range(j, j+3):
                        sum += self.plane_val[x, y]
                start_point[(i, j)] = sum
        self.three_by_three = start_point

    def sum_all(self):
        start_point = {}
        for dim in range(1,300-1):
            for i in range(300-dim):
                for j in range(300-dim):
                    start_point[(i, j, dim)] = np.sum(self.plane_val[i: i + dim + 1, j:j + dim + 1])
        self.three_by_three = start_point

    def print_largest(self):
        print("PART1: %s" % (max(self.three_by_three, key=self.three_by_three.get), ))

    def print_largest_p2(self):
        print("Size is one lower")
        print("PART2: %s" % (max(self.three_by_three, key=self.three_by_three.get), ))


def solve_p1(data_list):
    if __debug__:
        f_dev = FuelDevice(57)
        f_dev.print_cell((122, 79))
        f_dev = FuelDevice(39)
        f_dev.print_cell((217, 196))
        f_dev = FuelDevice(71)
        f_dev.print_cell((101, 153))
    else:
        f_dev = FuelDevice(int(data_list[0]))
        f_dev.sum_three()
        f_dev.print_largest()


def solve_p2(data_list):
    f_dev = FuelDevice(int(data_list[0]))
    f_dev.sum_all()
    f_dev.print_largest_p2()


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    solve_p1(data_list)
    solve_p2(data_list)


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
