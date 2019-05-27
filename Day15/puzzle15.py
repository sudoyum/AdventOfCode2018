#!/usr/bin/env python3

import os
import sys

import numpy as np

from collections import deque
from collections import OrderedDict


class BreakIt(Exception):
    pass


class Creature(object):
    def __init__(self, creature_type, creature_id, start):
        self.type = creature_type
        self.id = creature_id
        self.position = start
        self.hp = 200

    def is_alive(self):
        return self.hp > 0


class CombatGame(object):
    def __init__(self, data_list):
        self.game_over = False
        self.length = len(data_list)
        self.width = len(data_list[0])
        self.plane = np.zeros((self.width, self.length), dtype=np.int16)
        self.rounds = 0
        self.creatures = OrderedDict()
        self.goblins = []
        self.elves = []
        self.num_goblins = 0
        self.num_elves = 0
        creature_id = 2

        #P2 metrics
        self.elf_power = 3
        self.elf_attacks = 0
        self.gob_attacks = 0
        self.deaths = []

        for i in range(0, self.length):
            for j in range(0, self.width):
                if data_list[i][j] == '.':
                    self.plane[(i, j)] = 0
                elif data_list[i][j] == '#':
                    self.plane[(i, j)] = 1
                elif data_list[i][j] == 'G':
                    self.num_goblins += 1
                    self.plane[(i, j)] = creature_id
                    self.creatures[creature_id] = Creature('G', creature_id, (i, j))
                    self.goblins.append(creature_id)
                    creature_id += 1
                elif data_list[i][j] == 'E':
                    self.num_elves += 1
                    self.plane[(i, j)] = creature_id
                    self.creatures[creature_id] = Creature('E', creature_id, (i, j))
                    self.elves.append(creature_id)
                    creature_id += 1
        self.inum_elves = self.num_elves
        self.inum_gobs = self.num_goblins
        self.targeted = OrderedDict()
        for i in self.creatures.keys():
            self.targeted[i] = 0

    def debug_print_p2(self):
        print("INITIAL: %d ELVES, %d GOBLINS" % (self.inum_elves, self.inum_gobs))
        print("NUM_ELF_ATTACKS=%d" % (self.elf_attacks))
        print("NUM_GOB_ATTACKS=%d" % (self.gob_attacks))
        for tgt in self.targeted.keys():
            if self.creatures[tgt].type == 'G':
                print("G%d: %d, hp=%d" % (tgt, self.targeted[tgt], self.creatures[tgt].hp))
            elif self.creatures[tgt].type == 'E':
                print("E%d: %d, hp=%d" % (tgt, self.targeted[tgt], self.creatures[tgt].hp))
        for death in self.deaths:
            print("DEATH:%s%d, round=%d" % (self.creatures[death[0]].type, death[0], death[1]))

    def guess(self):
        return (float(self.inum_gobs * 200)/float(self.deaths[0][1]))/self.inum_elves

    def debug_print(self):
        print("Round %d:" % self.rounds)
        for j in range(0, self.length):
            for i in range(0, self.width):
                if self.plane[(j, i)] == 0:
                    sys.stdout.write('.')
                elif self.plane[(j, i)] == 1:
                    sys.stdout.write('#')
                else:
                    sys.stdout.write(self.creatures[self.plane[(j, i)]].type)
            sys.stdout.write('\n')
        sys.stdout.write('\n')

    # P1 question
    def battle_outcome(self):
        total_hp = 0
        for i in range(0, self.length):
            for j in range(0, self.width):
                bf_id = self.plane[(i, j)]
                if bf_id > 1:
                    if self.creatures[bf_id].is_alive():
                        total_hp += self.creatures[bf_id].hp
                        #print("hp=%d, id=%d" % (self.creatures[bf_id].hp, self.creatures[bf_id].id))
        #print("rounds=%d, total_hp=%d" % (self.rounds, total_hp))
        return self.rounds * total_hp

    def get_adjacent(self, creature_id):
        # TODO: Better way to do this?
        curr_pos = self.creatures[creature_id].position
        curr_race = self.creatures[creature_id].type
        adjacent_squares = [(curr_pos[0], curr_pos[1] + 1),
                            (curr_pos[0], curr_pos[1] - 1),
                            (curr_pos[0] + 1, curr_pos[1]),
                            (curr_pos[0] - 1, curr_pos[1])]
        valid_squares = []
        cin_range = False
        for square in adjacent_squares:
            if not((square[0] >= self.width or square[0] < 0) or
               (square[1] >= self.length or square[1] < 0)):
                if self.plane[square] == 0:
                    valid_squares.append(square)
                elif self.plane[square] > 1:
                    if self.creatures[self.plane[square]].type != curr_race:
                        cin_range = True
                        valid_squares.append(square)
        return valid_squares, cin_range

    def get_adjacent_open(self, creature_id=None, curr_pos=None):
        # TODO: Better way to do this?
        if creature_id:
            curr_pos = self.creatures[creature_id].position
        try:
            adjacent_squares = [(curr_pos[0], curr_pos[1] + 1),
                            (curr_pos[0], curr_pos[1] - 1),
                            (curr_pos[0] + 1, curr_pos[1]),
                            (curr_pos[0] - 1, curr_pos[1])]
        except TypeError as e:
            print("what?")
        valid_squares = []
        for square in adjacent_squares:
            if not((square[0] >= self.width or square[0] < 0) or
               (square[1] >= self.length or square[1] < 0)):
                if self.plane[square] == 0:
                    valid_squares.append(square)
        valid_squares.sort(key=lambda x: x[1])
        valid_squares.sort(key=lambda x: x[0])
        return valid_squares

    # first_step, num_steps = self.get_path_dist(creature_id, square)
    # creature_id to target_square
    # https://www.youtube.com/watch?v=oDqjPvD54Ss
    # https://www.youtube.com/watch?v=KiCBXu4P-2Y
    def get_path_dist(self, creature_id, square):
        curr_pos = self.creatures[creature_id].position
        prev = np.zeros((self.width, self.length), dtype=np.int16)
        mapping = {}
        index = 1
        visited = np.zeros((self.width, self.length), dtype=np.bool)
        visited[curr_pos] = True
        queue = deque()
        queue.append(curr_pos)
        while queue:
            sq = queue.popleft()
            neighbors = self.get_adjacent_open(curr_pos=sq)
            for n in neighbors:
                if not visited[n]:
                    queue.append(n)
                    visited[n] = True
                    prev[n] = index
                    mapping[index] = sq
                    index += 1
        if not prev[square]:
            return (0, 0), 0
        else:
            path = []
            node = square
            while node:
                path.append(node)
                try:
                    node = mapping[prev[node]]
                except KeyError:
                    break
            return path[-2], len(path) - 1

    def end_condition(self):
        if self.num_elves == 0 or self.num_goblins == 0:
            print("GAME OVER")
            self.game_over = True
            return True
        return False

    def elf_deaths(self):
        for death in self.deaths:
            if self.creatures[death[0]].type == 'E':
                return True
        return False

    def attack(self, valid_squares, curr_race):
        adversaries = []
        for square in valid_squares:
            sq = self.plane[square]
            if sq > 1:
                if curr_race == 'G':
                    if self.plane[square] in self.elves:
                        adversaries.append(self.creatures[self.plane[square]])
                else:
                    if self.plane[square] in self.goblins:
                        adversaries.append(self.creatures[self.plane[square]])
        adversaries.sort(key=lambda x: x.hp)
        sorted_ids = [adversaries[0].id]
        for i in range(0, len(adversaries) - 1):
            if adversaries[i].hp == adversaries[i + 1].hp:
                sorted_ids.append(adversaries[i + 1].id)
            else:
                break
        try:
            for i in range(0, self.length):
                for j in range(0, self.width):
                    if self.plane[(i, j)] in sorted_ids:
                        chosen_tgt = self.plane[(i, j)]
                        raise BreakIt
        except BreakIt:
            pass

        if self.creatures[chosen_tgt].type == 'E':
            self.creatures[chosen_tgt].hp -= 3
            self.gob_attacks += 1
        else:
            self.creatures[chosen_tgt].hp -= self.elf_power
            self.elf_attacks += 1
        self.targeted[chosen_tgt] += 1

        if self.creatures[chosen_tgt].hp <= 0:
            self.deaths.append((chosen_tgt, self.rounds))
            self.plane[self.creatures[chosen_tgt].position] = 0
            if self.creatures[chosen_tgt].type == "G":
                self.goblins.remove(chosen_tgt)
                self.num_goblins -= 1
            else:
                self.elves.remove(chosen_tgt)
                self.num_elves -= 1

    def do_round(self):
        # Sort by reading order
        ordered_ids = []
        for i in range(0, self.length):
            for j in range(0, self.width):
                if self.plane[(i, j)] > 1:
                    if self.creatures[self.plane[(i, j)]].is_alive():
                        ordered_ids.append(self.plane[i, j])

        for creature_id in ordered_ids:
            curr_race = self.creatures[creature_id].type
            valid_squares, cin_range = self.get_adjacent(creature_id)

            # Need this check for KIA creatures, as to not remove from for list
            if self.creatures[creature_id].is_alive():
                # Combat
                if cin_range:
                    self.attack(valid_squares, curr_race)
                else:
                    # Move
                    if self.creatures[creature_id].type == 'G':
                        targets = self.elves
                    else:
                        targets = self.goblins
                    if len(targets) == 0:
                        self.game_over = True
                        return
                    #identify all squares that targets can move to
                    all_squares = []
                    for target in targets:
                        all_squares += self.get_adjacent_open(creature_id=target)
                    #square fewest steps away
                    sorted_dists = []
                    lowest = 1000000
                    first_dest = None
                    for square in all_squares:
                        first_step, num_steps = self.get_path_dist(creature_id, square)
                        if num_steps > 0:
                            if num_steps < lowest:
                                lowest = num_steps
                                first_dest = first_step
                            sorted_dists.append((num_steps, first_step, square))
                    if len(sorted_dists) != 0:
                        #Update state
                        self.plane[self.creatures[creature_id].position] = 0
                        self.plane[first_dest] = creature_id
                        self.creatures[creature_id].position = first_dest
                    # APPARENTLY UNITS CAN MOVE AND ATTACK IN ONE ROUND COOL
                    valid_squares, cin_range = self.get_adjacent(creature_id)
                    if cin_range:
                        self.attack(valid_squares, curr_race)

        self.rounds += 1


def solve_p1(data_list):
    DEBUG_NUM = 1000000
    game = CombatGame(data_list)
    while not game.game_over:# and DEBUG_NUM > 0:
        game.do_round()
        DEBUG_NUM -= 1
    #game.debug_print()
    print("PART1: %d" % game.battle_outcome())


def solve_p2(data_list):
    elf_deaths = False
    game = CombatGame(data_list)
    game.elf_power = 3
    while not game.game_over:
        game.do_round()
    #game.debug_print_p2()
    guess = game.guess() * 2
    if guess < 4:
        guess = 4
    #print("GUESS=%d" % guess)
    while not elf_deaths:
        game = CombatGame(data_list)
        game.elf_power = guess
        #print("Guess=%d" % guess)
        while not game.game_over:
            game.do_round()
        elf_deaths = game.elf_deaths()
        guess -= 1
    optimal = guess + 2
    game = CombatGame(data_list)
    game.elf_power = optimal
    while not game.game_over:
         game.do_round()
    #print("OPTIMAL=%d" % optimal)
    print("PART2: %d" % game.battle_outcome())


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    solve_p1(data_list)
    solve_p2(data_list)


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
