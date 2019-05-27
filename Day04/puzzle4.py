#!/usr/bin/env python3

import os
import re
import sys

from collections import Counter
from collections import defaultdict
from datetime import datetime


fmt = "%Y-%m-%d %H:%M"


def most_common(lst):
    return max(set(lst), key=lst.count)


def num_common(lst):
    return Counter(lst).most_common()[0][1]


def solve_p1(sorted_vals):
    state = 0
    guards = {}
    guard_freq = {}
    for val in sorted_vals:
        m2 = re.search(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] Guard #(\d+)", val)
        if m2 and state == 0:
            if m2.group(6) not in guards.keys():
                guards[m2.group(6)] = 0
            current_guard = m2.group(6)
            state = 1
        if state == 1 or state == 0:
            m = re.search(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] falls asleep", val)
            if m:
                start_time = int(m.group(5))
                state = 2
        if state == 2:
            m = re.search(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] wakes up", val)
            if m:
                end_time = int(m.group(5))
                state = 0 
                guards[current_guard] = guards[current_guard] + (end_time - start_time)
                nums = []
                for i in range(start_time, end_time):
                     nums.append(i)
                if current_guard in guard_freq.keys():
                     guard_freq[current_guard] += nums
                else:
                     guard_freq[current_guard] = nums
    
    guard = max(guards.items(),  key=lambda x: x[1])
    print("PART1: %d" % (int(guard[0]) * most_common(guard_freq[guard[0]])))

    largest = 0
    for k, v in guard_freq.items():
        if num_common(v) > largest:
            guard_most = k
            minute_most = most_common(v)  
            largest = num_common(v)
    print("PART2: %d" % (int(guard_most) * minute_most))


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()

    line_dict = defaultdict()
    for line in data_list:
        m = re.search(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)", line.strip('\n'))
        if m:
            datestr = "%s-%s-%s %s:%s" % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
            line_dict[line] = datetime.strptime(datestr, fmt)
    time_sorted = sorted(line_dict, key=line_dict.get)
    solve_p1(time_sorted)


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

