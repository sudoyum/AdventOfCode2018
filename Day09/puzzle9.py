#!/usr/bin/env python3

import os
import re
import sys

# deque insert/remove no faster than list in current implementation
from collections import deque


#TODO: Rewrite with LinkedList. Left running and eventually finished after a couple hours for Part2
#TODO: Rewrite actually using deque correctly
class MarbleGame(object):
    def __init__(self, num_players, last_marble):
        self.num_players = num_players
        self.last_marble = last_marble
        self.circle = [0, 1]
        self.circle_len = 2
        self.current_index = 1
        self.current_marble = 2
        self.current_player = 1
        self.game_over = False
        self.scores = {}
        for i in range(1, num_players + 1):
            self.scores[str(i)] = 0

    def _one_clockwise(self):
        return (self.current_index + 1) % len(self.circle)

    def _two_clockwise(self):
        return (self.current_index + 2) % len(self.circle)

    def _print_game(self):
        sys.stdout.write("[%d] " % self.current_player)
        for i in range(0, self.circle_len):
            if i == self.current_index:
                sys.stdout.write("(%d)" % self.circle[i])
            else:
                sys.stdout.write("%d" % self.circle[i])
            sys.stdout.write(" ")
        sys.stdout.write("\n")

    # implementation in Part1, thought len() was costly.. was wrong
    # python3 -O -m cProfile puzzle9.py test9_3.txt
    def _index_between_p1(self):
        if self._two_clockwise() < self._one_clockwise():
            return len(self.circle)
        elif self._two_clockwise() > self._one_clockwise():
            return self._two_clockwise()

    def _index_between(self):
        two = (self.current_index + 2) % self.circle_len
        one = (self.current_index + 1) % self.circle_len
        if two < one:
            return self.circle_len
        elif two > one:
            return two

    def _update_state(self):
        self.current_player += 1
        if self.current_player == self.num_players + 1:
            self.current_player = 1
        self.current_marble += 1

    def _score(self):
        #player keeps marble
        self.scores[str(self.current_player)] += self.current_marble

        # remove seven to the left of current index
        removal_index = self.current_index - 7
        if removal_index < 0:
            removal_index += len(self.circle)

        # add removed to score
        self.scores[str(self.current_player)] += self.circle[removal_index]
        del self.circle[removal_index]
        self.circle_len -= 1
        self.current_index = removal_index

    def _game_turn(self):
        if self.current_marble == self.last_marble:
            self.game_over = True

        new_curr_index = self._index_between()
        if self.current_marble % 23 == 0:
            self._score()
        else:
            self.circle.insert(new_curr_index, self.current_marble)
            self.circle_len += 1
            self.current_index = new_curr_index
        self._update_state()

    def play_game(self):
        while not self.game_over:
            if __debug__:
                self._print_game()
            self._game_turn()

    def print_high_score(self):
        if __debug__:
            self._print_game()
        return max(self.scores.values())


def solve_p1(n_players, last_marble):
    game = MarbleGame(n_players, last_marble)
    game.play_game()
    print("PART1: %d" % game.print_high_score())


def solve_p2(n_players, last_marble):
    game = MarbleGame(n_players, last_marble * 100)
    game.play_game()
    print("PART2: %d" % game.print_high_score())


def format_input(f_name):
    with open(f_name, "r") as file:
        data = file.read().splitlines()
    for line in data:
        match = re.search(r"(\d+) players; last marble is worth (\d+) points", line)
        if match:
            n_players = int(match.group(1), 10)
            last_marble = int(match.group(2), 10)
            solve_p1(n_players, last_marble)
            solve_p2(n_players, last_marble)
        else:
            print("Input did not match regex")


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
