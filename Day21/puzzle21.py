#!/usr/bin/env python3

import os
import re
import sys


class InstructionParser(object):
    def __init__(self, pc_reg, program):
        self.program = program
        self.pc_reg = pc_reg
        self.ip = 0
        self.regs = [0] * 6
        self.debug_p1 = True
        self.test_once = 2
        self.do_again = True
        self.do_once = True

    # [('bori', 0), ('borr', 1), ('seti', 2), ('mulr', 3), ('setr', 4), ('addr', 5), ('gtir', 6), ('eqir', 7),
    # ('gtri', 8), ('bani', 9), ('muli', 10), ('gtrr', 11), ('banr', 12), ('eqri', 13), ('addi', 14), ('eqrr', 15)]
    def do_instruction(self):
        opcode, a, b, c = self.program[self.ip]

        self.regs[self.pc_reg] = self.ip

        if opcode == "bori": self.regs[c] = self.regs[a] | b
        elif opcode == "borr": self.regs[c] = self.regs[a] | self.regs[b]
        elif opcode == "seti": self.regs[c] = a
        elif opcode == "mulr": self.regs[c] = self.regs[a] * self.regs[b]
        elif opcode == "setr": self.regs[c] = self.regs[a]
        elif opcode == "addr": self.regs[c] = self.regs[a] + self.regs[b]
        elif opcode == "gtir": self.regs[c] = 1 if a > self.regs[b] else 0
        elif opcode == "eqir": self.regs[c] = 1 if a == self.regs[b] else 0
        elif opcode == "gtri": self.regs[c] = 1 if self.regs[a] > b else 0
        elif opcode == "bani": self.regs[c] = self.regs[a] & b
        elif opcode == "muli": self.regs[c] = self.regs[a] * b
        elif opcode == "gtrr": self.regs[c] = 1 if self.regs[a] > self.regs[b] else 0
        elif opcode == "banr": self.regs[c] = self.regs[a] & self.regs[b]
        elif opcode == "eqri": self.regs[c] = 1 if self.regs[a] == b else 0
        elif opcode == "addi": self.regs[c] = self.regs[a] + b
        elif opcode == "eqrr": self.regs[c] = 1 if self.regs[a] == self.regs[b] else 0
        else:
            print("didn't find opcode")
            sys.exit(1)

        self.ip = self.regs[self.pc_reg]
        self.ip += 1

def solve_p1_p2(pc_reg, program):
    prog_len = len(program)
    if True:
        parser = InstructionParser(pc_reg, program)
        while True:
            parser.do_instruction()
            if parser.ip >= prog_len:
                break
        print("PART1: %d" % parser.regs[0])
    else:
        parser = InstructionParser(pc_reg, program)
        parser.regs[0] = 1
        while True:
            parser.do_instruction()
            if parser.ip >= prog_len:
                break
        print("PART2: %d" % parser.regs[0])


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    match = re.search(r"ip (\d+)", data_list.pop(0))
    if match:
        pc_reg = match.group(1)
    else:
        print("no pc line?")
        sys.exit(1)
    program = []
    for data in data_list:
        match = re.search(r"([a-z0-9\s]+)", data)
        if match:
            inst = match.group(1).split(' ')
            inst_new = [inst.pop(0).strip()]
            for item in inst:
                inst_new.append(int(item.strip()))
            program.append(inst_new)
        else:
            print("no match?")
            sys.exit(1)

    solve_p1_p2(int(pc_reg), program)


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
