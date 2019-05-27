#!/usr/bin/env python3

import os
import sys

import numpy as np


# TODO: reconsider data structure
class PotGarden(object):
    CENTER = 10000

    def __init__(self, initial_state, steps):
        self.iteration = 0
        self.plane = np.zeros(self.CENTER * 2, dtype=np.int16)
        self.low = 0
        high = 0
        for i in range(0, len(initial_state)):
            if initial_state[i] == '#':
                self.plane[i + self.CENTER] = 1
                if i > high:
                    high = i
        self.high = high
        self.steps = []

        for step in steps:
            arr = np.zeros(5, dtype=np.int16)
            for i in range(0, len(step) - 1):
                if step[i] == '#':
                    arr[i] = 1
            if step.endswith('#'):
                transition = 1
            else:
                transition = 0
            self.steps.append((arr, transition))
        # remove lame all zero step

    def print_state(self):
        sys.stdout.write('%d: ' % self.iteration)
        for i in range(self.CENTER + self.low, self.CENTER + self.high + 1):
            if self.plane[i]:
                sys.stdout.write('#')
            else:
                sys.stdout.write('.')
        sys.stdout.write('\n')

    def do_iteration(self):
        self.iteration += 1
        replace_index = []
        for i in range(self.CENTER + self.low - 5, self.high + self.CENTER):
            for step in self.steps:
                if np.array_equal(step[0], self.plane[i:i + 5]):
                    replace_index.append((i + 2, step[1]))
                    if i + 2 - self.CENTER < self.low:
                        self.low = i + 2 - self.CENTER
                    if i + 2 - self.CENTER > self.high:
                        self.high = i + 2 - self.CENTER

        for i in range(self.low + self.CENTER, self.high + 4 + self.CENTER):
            self.plane[i] = 0

        for index in replace_index:
            self.plane[index[0]] = index[1]

    def sum_indeces(self):
        total = 0
        for i in range(self.low + self.CENTER, self.high + 1 + self.CENTER):
            if self.plane[i]:
                total += i - self.CENTER
        return total


def solve_p1_p2(initial_state, steps):
    garden = PotGarden(initial_state, steps)
    #garden.print_state()
    sum_list = []
#    for i in range(200):
#         garden.do_iteration()
#         sum = garden.sum_indeces()
#         sum_list.append(sum)
#        if sum not in seen:
#            seen.add(sum)
#        else:
#            print("MATCH=(i=%d, %d)" % (i, sum))
        #garden.print_state()
    for i in range(1, len(sum_list)):
        print("diff=%d, i=%d, sum=%d" % ((sum_list[i]-sum_list[i-1]), i, sum_list[i]))
    print("PART1: %d" % (garden.sum_indeces()))
    # i = 199, sum=6811
    total = 6811 + (50000000000 - 200) * 34
    print("PART2: %d" % total)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    initial_state = data_list.pop(0).split(' ')[2]
    data_list.pop(0)
    steps = []
    for data in data_list:
        steps.append(data.replace(" => ", ''))
    if __debug__:
        print(initial_state)
        print(len(steps))

    solve_p1_p2(initial_state, steps)


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


