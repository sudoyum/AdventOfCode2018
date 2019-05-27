#!/usr/bin/env python3

import os
import re
import sys

from collections import defaultdict


def get_deps(steps):
    deps = defaultdict(list)
    while True:
        count = 0
        for step in steps:
            if step[0] not in deps[step[1]]:
                deps[step[1]].append(step[0])
        for key, values in deps.copy().items():
            for vals in values:
                for v in deps[vals]:
                    if v not in deps[key]:
                        deps[key].append(v)
                        count += 1
        if count == 0:
            break
    return deps


def solve_p1(steps):
    finished = []
    possibles = []

    deps = get_deps(steps)
    while True:
        for key, value in deps.items():
            all_finished = True
            for c in value:
                if c not in finished:
                    all_finished = False
                    break
            if key not in finished and all_finished and key not in possibles:
                possibles.append(key)
        if len(possibles) == 0:
            break
        possibles.sort()
        finished.append(possibles.pop(0))
    print("PART1: %s" % ''.join(finished))


def solve_p2(steps):
    finished = []
    in_progress = []
    possibles = []

    total_time = 0
    total_occupied = 0
    deps = get_deps(steps)
    while True:
        for key, value in deps.items():
            all_finished = True
            for c in value:
                if c not in finished:
                    all_finished = False
                    break
            if key not in finished and all_finished and key not in possibles and key not in [i[0] for i in in_progress]:
                possibles.append(key)
        if len(possibles) == 0 and len(in_progress) == 0:
            break

        possibles.sort()
        while total_occupied < 5 and len(possibles) > 0:
            in_progress.append((possibles.pop(0), total_time))
            total_occupied += 1
        for task in in_progress:
            if (total_time - task[1] - (ord(task[0]) - 5)) == 0:
                finished.append(task[0])
                total_occupied -= 1
        for task in finished:
            if task in [i[0] for i in in_progress]:
                in_progress = [i for i in in_progress if i[0] != task]
        total_time += 1
    print("PART2: %d" % total_time)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()

    steps = []
    for line in data_list:
        match = re.search("Step (\w) must be finished before step (\w) can begin", line.strip('\n'))
        if match:
            steps.append((match.group(1), match.group(2)))
        else:
            print("Regex messed up")
            sys.exit(1)
    solve_p1(steps)
    solve_p2(steps)


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