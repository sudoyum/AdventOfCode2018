#!/usr/bin/env python3

import os
import sys


#TODO: part2 take 2m30s
class HotChoclate(object):
    def __init__(self, num):
        self.iteration_num = 0
        self.num_recipes = num
        self.scores = [3, 7]
        self.elf1 = 0
        self.elf2 = 1
        self.input_list = None

    def debug_print(self):
        sys.stdout.write("%d: " % self.iteration_num)
        for i in range(len(self.scores)):
            if i == self.elf1:
                sys.stdout.write("(%d) " % self.scores[i])
            elif i == self.elf2:
                sys.stdout.write("[%d] " % self.scores[i])
            else:
                sys.stdout.write("%d " % self.scores[i])
        sys.stdout.write("\n")

    def do_recipe(self):
        sum = self.scores[self.elf1] + self.scores[self.elf2]
        # TODO: better way to do this - decimal mask?
        sum_str = str(sum)
        recipe = []
        for i in range(0, len(sum_str)):
            #print("%d" % int(sum_str[i]))
            recipe.append(int(sum_str[i]))
        self.scores += recipe

        move1 = self.scores[self.elf1] + 1
        move2 = self.scores[self.elf2] + 1
        self.elf1 += move1
        self.elf2 += move2
        self.elf1 %= len(self.scores)
        self.elf2 %= len(self.scores)
        self.iteration_num += 1

    def print_ten_after(self, index):
        for i in range(0, 10):
            sys.stdout.write("%d" % self.scores[index + i])
        sys.stdout.write("\n")

    def pattern_matches(self):
        indexes = []
        for i in range(len(self.scores)):
            if self.scores[i:i + len(self.input_list)] == self.input_list:
                indexes.append((i, i + len(self.input_list)))
        if indexes:
            return indexes[0][0]
        else:
            return 0


def solve_p1(num):
    game = HotChoclate(num)
    for i in range(100000):
        game.do_recipe()
    if __debug__:
        game.print_ten_after(5)
        game.print_ten_after(18)
        game.print_ten_after(2018)
    sys.stdout.write("PART1: ")
    game.print_ten_after(47801)

def solve_p2(num):
    game = HotChoclate(num)
    input_list = [0, 4, 7, 8, 0, 1]
    test_input_list = [5, 1, 5, 8, 9]
    test_input_list = [0, 1, 2, 4, 5]
    test_input_list = [5, 9, 4, 1, 4]
    game.input_list = input_list
    for i in range(100000000):
        game.do_recipe()
        if __debug__:
            if i == 100000:
                print("PART2: %d" % game.pattern_matches())
            if i == 1000000:
                print("PART2: %d" % game.pattern_matches())

    print("PART2: %d" % game.pattern_matches())

def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    solve_p1(int(data_list[0]))
    solve_p2(int(data_list[0]))


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

