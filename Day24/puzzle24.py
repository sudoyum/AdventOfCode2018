#!/usr/bin/env python3

import copy
import os
import re
import sys

from collections import defaultdict

IMMUNE_TYPE = 0xff100
INFECT_TYPE = 0xff200

# Gross storage of state, use of deepcopy
# Stalemate situation for part 2 caused infinite loop
class ArmyGroup(object):
    def __init__(self, num, unit_type, units, hp, attack, a_type, initiative, extras):
        self.group_num = num
        self.units = units
        self.hp = hp
        self.attack = attack
        self.a_type = a_type
        self.initiative = initiative
        self.weakness = []
        self.immune = []
        self.efp = units * attack
        self.dmg_list = []
        self.tgt = None
        self.stale_tgt = False
        self.attacked = False

        if unit_type:
            self.type = IMMUNE_TYPE
        else:
            self.type = INFECT_TYPE

        self.id = self.type | self.group_num
        if extras is not None:
            match = re.search(r"weak to (\w+)(, \w+)?(, \w+)?", extras)
            if match:
                for hit in match.groups():
                    if hit is not None:
                        hit = hit.strip(" ,")
                        self.weakness.append(hit)
            match = re.search(r"immune to (\w+)(, \w+)?(, \w+)?", extras)
            if match:
                for hit in match.groups():
                    if hit is not None:
                        hit = hit.strip(" ,")
                        self.immune.append(hit)

    def is_alive(self):
        return self.units > 0

    def set_efp(self):
        self.efp = self.units * self.attack

    def efp_enemies(self, imm_unit, inf_unit):
        if self.type == IMMUNE_TYPE:
            if imm_unit.a_type in inf_unit.weakness:
                self.dmg_list.append((inf_unit, 2 * self.units * self.attack))
            elif imm_unit.a_type in inf_unit.immune:
                self.dmg_list.append((inf_unit, 0))
            else:
                self.dmg_list.append((inf_unit, self.units * self.attack))
        elif self.type == INFECT_TYPE:
            if inf_unit.a_type in imm_unit.weakness:
                self.dmg_list.append((imm_unit, 2 * self.units * self.attack))
            elif inf_unit.a_type in imm_unit.immune:
                self.dmg_list.append((imm_unit, 0))
            else:
                self.dmg_list.append((imm_unit, self.units * self.attack))

    def take_dmg(self, dmg):
        self.units -= dmg/self.hp

    def take_from_opp(self, opp):
        if opp.a_type in self.weakness:
            opp_dmg = 2 * opp.units * opp.attack
        elif opp.a_type in self.immune:
            opp_dmg = 0
        else:
            opp_dmg = opp.units * opp.attack
        kills = int(opp_dmg/self.hp)
        self.units -= int(opp_dmg/self.hp)
        return kills

    def effective_power(self):
        return self.units * self.attack


def print_from_id(id, id2):
    if (id & 0xfff00) == INFECT_TYPE:
        print("Infect %d attacks Immune %d" % ((id & 0xff), (id2 & 0xff)))
    else:
        print("Immune %d attacks Infect %d" % ((id & 0xff), (id2 & 0xff)))


class Battlefield(object):
    def __init__(self, armies):
        self.armies = armies
        self.immune = [i for i in self.armies if i.type == IMMUNE_TYPE]
        self.infected = [i for i in self.armies if i.type == INFECT_TYPE]
        self.done = False
        self.turn = 0
        self.winner = None

    def debug_print(self):
        print("Immune System:")
        for im in self.immune:
            print("Group %d contains %d units" % (im.group_num, im.units))
        print("Infect System:")
        for inf in self.infected:
            print("Group %d contains %d units" % (inf.group_num, inf.units))

    def debug_ordering(self):
        for army in self.armies:
            if army.type == IMMUNE_TYPE:
                sys.stdout.write("Immune %d: " % army.group_num)
            else:
                sys.stdout.write("Infection %d: " % army.group_num)
            sys.stdout.write(str(army.dmg_list))
            sys.stdout.write("\n")

    def get_winning_size(self):
        total = 0
        if len(self.infected) == 0:
            for army in self.immune:
                total += army.units
        else:
            for army in self.infected:
                total += army.units
        return total

    def target_selection(self):
        for army in self.armies:
            army.set_efp()
            army.stale_tgt = False
            army.attacked = False
            army.dmg_list = []

        self.armies.sort(key=lambda x: (x.efp, x.initiative), reverse=True)
        for army in self.armies:
            if army.type == INFECT_TYPE:
                for imm in self.immune:
                    army.efp_enemies(imm, army)
                army.dmg_list.sort(key=lambda x: (x[1], x[0].efp, x[0].initiative), reverse=True)
            else:
                for inf in self.infected:
                    army.efp_enemies(army, inf)
                army.dmg_list.sort(key=lambda x: (x[1], x[0].efp, x[0].initiative), reverse=True)

        selected = []
        for army in self.armies:
            tgt_found = False
            for i in range(0, len(army.dmg_list)):
                if army.dmg_list[i][0].id not in selected:
                    if army.dmg_list[i][1] != 0:
                        selected.append(army.dmg_list[i][0].id)
                        tgt_found = True
                    army.tgt = army.dmg_list[i]
                    break
            if not tgt_found:
                army.stale_tgt = True


        # Attack Phase
        kills = 0
        self.armies.sort(key=lambda x: x.initiative, reverse=True)
        num = 0
        while True:
            self.armies[num].attacked = True
            if not self.armies[num].stale_tgt:
                for m_army in self.armies:
                    if m_army.id == self.armies[num].tgt[0].id:
                        #print_from_id(self.armies[num].id, m_army.id)
                        kills += m_army.take_from_opp(self.armies[num])
                        break
            if len([i for i in self.armies if i.attacked]) == len(self.armies):
                break
            num += 1

        self.armies = [i for i in self.armies if i.is_alive()]
        self.immune = [i for i in self.armies if i.type == IMMUNE_TYPE]
        self.infected = [i for i in self.armies if i.type == INFECT_TYPE]
        if len(self.immune) == 0 or len(self.infected) == 0 or kills == 0:
            self.done = True
            if len(self.immune) == 0 or kills == 0:
                self.winner = INFECT_TYPE
            else:
                self.winner = IMMUNE_TYPE


def solve_p1(armies):
    bf = Battlefield(armies)
    while not bf.done:
        bf.target_selection()
    print("PART1: %d" % bf.get_winning_size())


def solve_p2(armies):
    win = False
    boost = 1
    base_armies = copy.deepcopy(armies)
    while not win:
        for army in armies:
            if army.type == IMMUNE_TYPE:
                army.attack += boost
        bf = Battlefield(armies)
        while not bf.done:
            bf.target_selection()
        if bf.winner == IMMUNE_TYPE:
            win = True
            print("PART2: %d" % bf.get_winning_size())
        else:
            boost += 1
            armies = copy.deepcopy(base_armies)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()

    infgroup_num = 1
    immgroup_num = 1
    armies = []
    immune = True
    for data in data_list:
        match = re.search(r"Infection:", data)
        if match:
            immune = False

        match = re.search(r"(\d+) units each with (\d+) hit points (\([a-zA-Z;,\s]+\))?", data)
        match_end = re.search(r"that does (\d+) (\w+) damage at initiative (\d+)", data)

        if match and match_end:
            group_num = immgroup_num if immune else infgroup_num
            armies.append(ArmyGroup(group_num,
                                    immune,
                                    int(match.group(1)),
                                    int(match.group(2)),
                                    int(match_end.group(1)),
                                    match_end.group(2),
                                    int(match_end.group(3)),
                                    match.group(3)))
            if immune:
                immgroup_num += 1
            else:
                infgroup_num += 1
    orig_armies = copy.deepcopy(armies)
    solve_p1(copy.deepcopy(orig_armies))
    solve_p2(copy.deepcopy(orig_armies))


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
