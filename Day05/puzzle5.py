#!/usr/bin/env python3

import copy
import os
import string
import sys


def check_done(protein):
    for i in range(0, len(protein) - 1):
        if abs(ord(protein[i]) - ord(protein[i+1])) == 32:
            print("Match=%c%c" % (protein[i], protein[i+1]))
            return True
    return False


def minimize_protein(protein):
    i = 0
    new_p = []
    while True:
        if abs(ord(protein[i]) - ord(protein[i+1])) == 32:
            j = 2
            while True:
                if 0 == len(new_p) or (i + j >= len(protein)):
                    break
                if abs(ord(new_p[-1]) - ord(protein[i+j])) == 32:
                    new_p.pop()
                    j += 1
                else:
                    break
            i += j
        else:
            new_p.append(protein[i])
            i += 1
        if i >= len(protein) - 1:
            if i < len(protein): 
                new_p.append(protein[i])
            break
    return ''.join(new_p)


def solve_p1(protein):
    print("PART1: %d" % len(minimize_protein(protein)))


def remove_protein(protein, character):
    protein = protein.replace(character, "").replace(character.upper(), "")
    return len(minimize_protein(protein))
 

def solve_p2(protein):
    removed_lens = []
    for character in string.ascii_lowercase:
        removed_lens.append(remove_protein(protein, character))
    print("PART2: %d" % min(removed_lens))


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    protein = data_list[0].strip('\n')
    solve_p1(protein)
    solve_p2(protein)


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

