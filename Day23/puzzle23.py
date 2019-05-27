#!/usr/bin/env python3

import os
import re
import sys

import numpy as np


class NanoBot(object):
    def __init__(self, coord, radius):
        x, y, z = coord.split(',')
        self.pos = (int(x), int(y), int(z))
        self.norm_pos = None
        self.r = int(radius)
        self.mdist = None
        if self.r >= sys.maxsize:
            print("Over")
        if self.pos[0] >= sys.maxsize or\
           self.pos[1] >= sys.maxsize or\
           self.pos[2] >= sys.maxsize:
            print("Over")


class Teleportation(object):
    def __init__(self, bot_list):
        bot_list.sort(key=lambda b: b.r, reverse=True)
        self.bot_list = bot_list
        self.strongest = self.bot_list[0]
        self.in_range = []
        self.plane = None

    def set_manhattan(self):
        for bot in self.bot_list:
            mdist = 0
            for i in range(0, 3):
                 mdist += abs(self.strongest.pos[i] - bot.pos[i])
            bot.mdist = mdist

    def set_in_range(self):
        for bot in self.bot_list:
            if bot.mdist <= self.strongest.r:
                self.in_range.append(bot)

    def find_coordinate(self):
        max_x = sorted(self.bot_list, key=lambda b: b.pos[0], reverse=True)[0].pos[0]
        min_x = sorted(self.bot_list, key=lambda b: b.pos[0])[0].pos[1]
        max_y = sorted(self.bot_list, key=lambda b: b.pos[1], reverse=True)[0].pos[1]
        min_y = sorted(self.bot_list, key=lambda b: b.pos[1])[0].pos[1]
        max_z = sorted(self.bot_list, key=lambda b: b.pos[2], reverse=True)[0].pos[2]
        min_z = sorted(self.bot_list, key=lambda b: b.pos[2])[0].pos[2]
        print("here")
        if min_x < 0:
            norm_x = abs(min_x)
            max_x += abs(min_x)
        else:
            norm_x = 0

        if min_y < 0:
            norm_y = abs(min_y)
            max_y += abs(min_y)
        else:
            norm_y = 0

        if min_z < 0:
            norm_z = abs(min_z)
            max_z += abs(min_z)
        else:
            norm_z = 0

        for bot in self.bot_list:
            bot.norm_post = (bot.pos[0]+norm_x, bot.pos[1] + norm_y, bot.pos[2] + norm_z)

        self.plane = np.zeros((max_x, max_y, max_z), dtype=np.int16)
        for bot in self.bot_list:
            for i in range(bot.norm_post[0]-bot.r, bot.norm_post[0] + bot.r):
                 for j in range(bot.norm_post[1] - bot.r, bot.norm_post[1]+bot.r):
                     for k in range(bot.norm_post[2]- bot.r, bot.norm_post[2]+bot.r):
                         dist = i*i + j*j + k*k
                         if bot.rsq >= dist:
                             self.plane[(i, j, k)] += 1



def solve_p1(bot_list):
    telep = Teleportation(bot_list)
    telep.set_manhattan()
    telep.set_in_range()
    print("PART1: %d" % len(telep.in_range))


def solve_p2(bot_list):
    telep = Teleportation(bot_list)
    telep.set_manhattan()
    telep.find_coordinate()
    print("PART2: %d")


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    bot_list = []
    for line in data_list:
        match = re.search(r"pos=<([-0-9,]+)>, r=(\d+)", line)
        if match:
            bot_list.append(NanoBot(match.group(1), match.group(2)))

    solve_p1(bot_list)
    #solve_p2(bot_list)


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


