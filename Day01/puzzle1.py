#!/usr/bin/env python3

import os
import sys


def solve_p1(freq_list):
    print("PART1: %d" % sum(freq_list))


def solve_p2(freq_list):
    found_freq = set()
    freq_res = 0

    while True:
        for freq in freq_list:
            if freq_res in found_freq:
                print("PART2: %d" % freq_res)
                sys.exit(1)
            else:
                found_freq.add(freq_res)
            freq_res += freq


def format_input(f_name):
    with open(f_name, "r") as file:
        freq_list = list(map(int, file.read().splitlines()))
    solve_p1(freq_list)
    solve_p2(freq_list)


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

