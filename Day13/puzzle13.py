#!/usr/bin/env python3

import os
import sys
from enum import Enum

import numpy as np


class Track(Enum):
    VERT_STRAIGHT = 0x1
    HORI_STRAIGHT = 0x2
    R_CURVE = 3
    L_CURVE = 4
    INTERSECTION = 5
    CART_UP = 6
    CART_DN = 7
    CART_LEFT = 8
    CART_RIGHT = 9


class CartTracks(object):
    def __init__(self, data_list):
        self.tick_count = 0
        self.first_crash = None
        self.crash = None
        width = len(max(data_list, key=len))
        length = len(data_list)
        if __debug__:
            print("length = %d" % length)
            print("width = %d" % width)
        plane = np.zeros((width, length), dtype=np.int16)
        cart_indices = []
        for j in range(0, length):
            for i in range(0, len(data_list[j])):
                if data_list[j][i] == "|":
                    plane[i, j] = Track.VERT_STRAIGHT.value
                elif data_list[j][i] == "-":
                    plane[i, j] = Track.HORI_STRAIGHT.value
                elif data_list[j][i] == "/":
                    plane[i, j] = Track.R_CURVE.value
                elif data_list[j][i] == "\\":
                    plane[i, j] = Track.L_CURVE.value
                elif data_list[j][i] == "+":
                    plane[i, j] = Track.INTERSECTION.value
                elif data_list[j][i] == "^":
                    plane[i, j] = Track.VERT_STRAIGHT.value
                    cart_indices.append([i, j, Track.CART_UP.value, 0])
                elif data_list[j][i] == "v":
                    plane[i, j] = Track.VERT_STRAIGHT.value
                    cart_indices.append([i, j, Track.CART_DN.value, 0])
                elif data_list[j][i] == ">":
                    plane[i, j] = Track.HORI_STRAIGHT.value
                    cart_indices.append([i, j, Track.CART_RIGHT.value, 0])
                elif data_list[j][i] == "<":
                    plane[i, j] = Track.HORI_STRAIGHT.value
                    cart_indices.append([i, j, Track.CART_LEFT.value, 0])
        self.width = width
        self.length = length
        self.plane = plane
        self.cart_indices = cart_indices

    # TODO: this function got ridiculous
    def tick(self):
        self.tick_count += 1
        # Carts should already be sorted top left to right?
        self.cart_indices = sorted(self.cart_indices, key=lambda k:[k[1], k[0]])

        cart_copy = self.cart_indices.copy()
        for index in cart_copy:
            if self.plane[index[0], index[1]] == Track.HORI_STRAIGHT.value:
                if index[2] == Track.CART_RIGHT.value:
                    index[0] += 1
                elif index[2] == Track.CART_LEFT.value:
                    index[0] -= 1
                else:
                    print("fail")
            elif self.plane[index[0], index[1]] == Track.VERT_STRAIGHT.value:
                if index[2] == Track.CART_UP.value:
                    index[1] -= 1
                elif index[2] == Track.CART_DN.value:
                    index[1] += 1
                else:
                    print("fail")
            # \
            elif self.plane[index[0], index[1]] == Track.L_CURVE.value:
                if index[2] == Track.CART_UP.value:
                    index[0] -= 1
                    index[2] = Track.CART_LEFT.value
                elif index[2] == Track.CART_DN.value:
                    index[0] += 1
                    index[2] = Track.CART_RIGHT.value
                elif index[2] == Track.CART_RIGHT.value:
                    index[1] += 1
                    index[2] = Track.CART_DN.value
                elif index[2] == Track.CART_LEFT.value:
                    index[1] -= 1
                    index[2] = Track.CART_UP.value
            # /
            elif self.plane[index[0], index[1]] == Track.R_CURVE.value:
                if index[2] == Track.CART_UP.value:
                    index[0] += 1
                    index[2] = Track.CART_RIGHT.value
                elif index[2] == Track.CART_DN.value:
                    index[0] -= 1
                    index[2] = Track.CART_LEFT.value
                elif index[2] == Track.CART_RIGHT.value:
                    index[1] -= 1
                    index[2] = Track.CART_UP.value
                elif index[2] == Track.CART_LEFT.value:
                    index[1] += 1
                    index[2] = Track.CART_DN.value
            elif self.plane[index[0], index[1]] == Track.INTERSECTION.value:
                if index[2] == Track.CART_UP.value:
                    if index[3] == 0:
                        index[0] -= 1
                        index[2] = Track.CART_LEFT.value
                    elif index[3] == 1:
                        index[1] -= 1
                    elif index[3] == 2:
                        index[0] += 1
                        index[2] = Track.CART_RIGHT.value
                elif index[2] == Track.CART_DN.value:
                    if index[3] == 0:
                        index[0] += 1
                        index[2] = Track.CART_RIGHT.value
                    elif index[3] == 1:
                        index[1] += 1
                    elif index[3] == 2:
                        index[0] -= 1
                        index[2] = Track.CART_LEFT.value
                elif index[2] == Track.CART_RIGHT.value:
                    if index[3] == 0:
                        index[1] -= 1
                        index[2] = Track.CART_UP.value
                    elif index[3] == 1:
                        index[0] += 1
                    elif index[3] == 2:
                        index[1] += 1
                        index[2] = Track.CART_DN.value
                elif index[2] == Track.CART_LEFT.value:
                    if index[3] == 0:
                        index[1] += 1
                        index[2] = Track.CART_DN.value
                    elif index[3] == 1:
                        index[0] -= 1
                    elif index[3] == 2:
                        index[1] -= 1
                        index[2] = Track.CART_UP.value
                index[3] += 1
                index[3] %= 3
            check = set()
            self.crash = []
            indeces = self.cart_indices.copy()
            for cart in indeces:
                if (cart[0], cart[1]) in check:
                    for cr in indeces:
                        if cart[0] == cr[0] and cart[1] == cr[1]:
                            self.cart_indices.remove(cr)
                    if self.first_crash is None:
                        self.first_crash = (cart[0], cart[1])
                else:
                    check.add((cart[0], cart[1]))
        if len(self.cart_indices) == 1:
            print("PART2: %s" % self.cart_indices[0])
            return True
        if len(self.cart_indices) % 2 == 0:
            print("even?")
        return False


def solve_p1_p2(data_list):
    cart_tracks = CartTracks(data_list)
    sanity = 0
    while 1:
        crash = cart_tracks.tick()
        if crash or sanity > 1000000:
            break
        else:
            sanity += 1
    print("PART1: %s" % (cart_tracks.first_crash,))


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    solve_p1_p2(data_list)


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


