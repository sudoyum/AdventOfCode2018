#!/usr/bin/env python3

import os
import sys


def solve_p1():
    print("PART1: %d")


def solve_p2():
    print("PART2: %d")


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    solve_p1()
    solve_p2()


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


