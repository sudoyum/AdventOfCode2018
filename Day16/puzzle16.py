#!/usr/bin/env python3

import operator
import os
import re
import sys

from collections import defaultdict


class InstructionParser(object):
    def __init__(self):
        self.regs = [0, 0, 0, 0]
        self.before_regs = None
        self.after_regs = None
        self.opcodes = defaultdict(list)
        self.solved_opcodes = {}
        self.act_like_three = 0

    def set_before(self, before_regs):
        self.before_regs = before_regs

    def set_after(self, after_regs):
        self.after_regs = after_regs

    def set_type(self, inst):
        a = inst[1]
        b = inst[2]
        c = inst[3]

        total_len = sum([len(v) for v in self.opcodes.values()])
        if (self.before_regs[a] + self.before_regs[b]) == self.after_regs[c]:
            self.opcodes['addr'].append(inst[0])
        if (self.before_regs[a] + b) == self.after_regs[c]:
            self.opcodes['addi'].append(inst[0])
        if (self.before_regs[a] * self.before_regs[b]) == self.after_regs[c]:
            self.opcodes['mulr'].append(inst[0])
        if (self.before_regs[a] * b) == self.after_regs[c]:
            self.opcodes['muli'].append(inst[0])
        if (self.before_regs[a] & self.before_regs[b]) == self.after_regs[c]:
            self.opcodes['banr'].append(inst[0])
        if (self.before_regs[a] & b) == self.after_regs[c]:
            self.opcodes['bani'].append(inst[0])
        if (self.before_regs[a] | self.before_regs[b]) == self.after_regs[c]:
            self.opcodes['borr'].append(inst[0])
        if (self.before_regs[a] | b) == self.after_regs[c]:
            self.opcodes['bori'].append(inst[0])
        if self.before_regs[a] == self.after_regs[c]:
            self.opcodes['setr'].append(inst[0])
        if a == self.after_regs[c]:
            self.opcodes['seti'].append(inst[0])

        if (1 == self.after_regs[c]) and (a > self.before_regs[b]) or\
           (0 == self.after_regs[c]) and (a <= self.before_regs[b]):
            self.opcodes['gtir'].append(inst[0])

        if (1 == self.after_regs[c]) and (self.before_regs[a] > b) or \
           (0 == self.after_regs[c]) and (self.before_regs[a] <= b):
            self.opcodes['gtri'].append(inst[0])

        if (1 == self.after_regs[c]) and (self.before_regs[a] > self.before_regs[b]) or \
           (0 == self.after_regs[c]) and (self.before_regs[a] <= self.before_regs[b]):
            self.opcodes['gtrr'].append(inst[0])

        if (1 == self.after_regs[c]) and (a == self.before_regs[b]) or\
           (0 == self.after_regs[c]) and (a != self.before_regs[b]):
            self.opcodes['eqir'].append(inst[0])

        if (1 == self.after_regs[c]) and (self.before_regs[a] == b) or \
           (0 == self.after_regs[c]) and (self.before_regs[a] != b):
            self.opcodes['eqri'].append(inst[0])

        if (1 == self.after_regs[c]) and (self.before_regs[a] == self.before_regs[b]) or \
           (0 == self.after_regs[c]) and (self.before_regs[a] != self.before_regs[b]):
            self.opcodes['eqrr'].append(inst[0])

        total_len_after = sum([len(v) for v in self.opcodes.values()])

        if (total_len_after - total_len) >= 3:
            self.act_like_three += 1

    def determine_opcode(self):
        for k, v in self.opcodes.items():
            self.opcodes[k] = set(v)

        solved = False
        while not solved:
            for k, v in self.opcodes.items():
                if len(v) == 1:
                    remove_val = v.pop()
                    self.solved_opcodes[k] = remove_val
                    del self.opcodes[k]
                    break
            for k, v in self.opcodes.items():
                if remove_val in v:
                     self.opcodes[k].remove(remove_val)

            if len(self.solved_opcodes.keys()) == 16:
                solved = True
        #print(sorted(self.solved_opcodes.items(), key=operator.itemgetter(1)))

    # [('bori', 0), ('borr', 1), ('seti', 2), ('mulr', 3), ('setr', 4), ('addr', 5), ('gtir', 6), ('eqir', 7),
    # ('gtri', 8), ('bani', 9), ('muli', 10), ('gtrr', 11), ('banr', 12), ('eqri', 13), ('addi', 14), ('eqrr', 15)]
    def do_instruction(self, inst):
        opcode, a, b, c = inst
        if opcode == 0: self.regs[c] = self.regs[a] | b
        if opcode == 1: self.regs[c] = self.regs[a] | self.regs[b]
        if opcode == 2: self.regs[c] = a
        if opcode == 3: self.regs[c] = self.regs[a] * self.regs[b]
        if opcode == 4: self.regs[c] = self.regs[a]
        if opcode == 5: self.regs[c] = self.regs[a] + self.regs[b]
        if opcode == 6: self.regs[c] = 1 if a > self.regs[b] else 0
        if opcode == 7: self.regs[c] = 1 if a == self.regs[b] else 0
        if opcode == 8: self.regs[c] = 1 if self.regs[a] > b else 0
        if opcode == 9: self.regs[c] = self.regs[a] & b
        if opcode == 10: self.regs[c] = self.regs[a] * b
        if opcode == 11: self.regs[c] = 1 if self.regs[a] > self.regs[b] else 0
        if opcode == 12: self.regs[c] = self.regs[a] & self.regs[b]
        if opcode == 13: self.regs[c] = 1 if self.regs[a] == b else 0
        if opcode == 14: self.regs[c] = self.regs[a] + b
        if opcode == 15: self.regs[c] = 1 if self.regs[a] == self.regs[b] else 0


def solve_p1(parsed_inst):
    ip = InstructionParser()
    for inst in parsed_inst:
        ip.set_before(inst[0])
        ip.set_after(inst[2])
        ip.set_type(inst[1])

    print("PART1: %d" % ip.act_like_three)
    ip.determine_opcode()


def solve_p2(program):
    ip = InstructionParser()
    for inst in program:
        ip.do_instruction(inst)
    print("PART2: %d" % ip.regs[0])


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    if "input16.txt" == f_name:
        parsed_inst = []
        reg_after = None
        reg_before = None
        for data in data_list:
            match_b = re.search(r"Before: \[([0-9,\s]+)", data)
            match_a = re.search(r"After:\s+\[([0-9,\s]+)", data)
            if match_b:
                reg_before = match_b.group(1).strip().split(',')
                reg_before_new = []
                for item in reg_before:
                    reg_before_new.append(int(item.strip()))
            elif match_a:
                reg_after = match_a.group(1).strip().split(',')
                reg_after_new = []
                for item in reg_after:
                    reg_after_new.append(int(item.strip()))
                if reg_after and reg_before and inst:
                        parsed_inst.append((reg_before_new, inst_new, reg_after_new))
            else:
                match = re.search(r"([0-9\s]+)", data)
                if match:
                    inst = match.group(1).split(' ')
                    inst_new = []
                    for item in inst:
                        inst_new.append(int(item.strip()))
        solve_p1(parsed_inst)
    elif "input16_p2.txt" == f_name:
        program = []
        for data in data_list:
            match = re.search(r"([0-9]+ [0-9]+ [0-9]+ [0-9]+)", data)
            if match:
                inst = match.group(1).split(' ')
                inst_new = []
                for item in inst:
                    inst_new.append(int(item.strip()))
                program.append(inst_new)
        solve_p2(program)
    else:
        print("pass in a correct input file")


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
