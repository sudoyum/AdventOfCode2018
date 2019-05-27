#!/usr/bin/env python3

import os
import sys

from collections import Counter


def solve_p1(box_ids):
    repeated_twice = 0
    repeated_thrice = 0
    for id in box_ids:
        counter = Counter(id)
        vals = list(counter.values())
        if vals.count(2):
            repeated_twice += 1
        if vals.count(3):
            repeated_thrice += 1

    if __debug__:
        print("repeated_twice = %d" % repeated_twice)
        print("repeated_thrice = %d" % repeated_thrice)
    print("PART1: %d" % (repeated_thrice * repeated_twice))


def single_diff(str1, str2):
    num_diffs = 0
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            num_diffs += 1
            if num_diffs > 1:
                return False
    return True


def get_diffed_str(str1, str2):
    diff_str = ""
    for i in range(0, len(str1)):
        if str1[i] == str2[i]:
            diff_str += str1[i]
    return diff_str


def solve_p2(box_ids):
    compare_index = 1
    for id in box_ids:
        for i in range(compare_index, len(box_ids)):
            if single_diff(id, box_ids[i]):
                if __debug__:
                    print(id)
                    print(box_ids[i])
                print("PART2: %s" % get_diffed_str(id, box_ids[i]))
                sys.exit(1)
        compare_index += 1


def format_input(f_name):
    with open(f_name, "r") as file:
        box_ids = file.read().splitlines()
    solve_p1(box_ids)
    solve_p2(box_ids)


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
