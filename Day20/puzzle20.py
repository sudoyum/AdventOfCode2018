#!/usr/bin/env python3

import copy
import os
import re
import sys

from collections import defaultdict, OrderedDict

import numpy as np


class RegularMap(object):
    MAX_X = MAX_Y = 20000
    WALL = 0
    TRAVELED = 1
    EW_DOOR = 2
    NS_DOOR = 3
    EMPTY_ROOM = 4
    START = 5

    def __init__(self, routes):
        self.plane = np.zeros((self.MAX_X, self.MAX_Y), dtype=np.int8)
        self.room_plane = np.zeros((self.MAX_X, self.MAX_Y), dtype=np.int32)
        self.routes = routes
        self.curr_pos_x = 0
        self.curr_pos_y = 0
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.distances = []
        self.plane[(0, 0)] = self.START
        self.rooms = []

    def print_map(self):
        self.plane[(0, 0)] = self.START
        for y in range(self.min_y-1, self.max_y + 2):
            for x in range(self.min_x-1, self.max_x + 2):
                if self.plane[(x, y)] == self.WALL:
                    sys.stdout.write('#')
                elif self.plane[(x, y)] == self.EW_DOOR:
                    sys.stdout.write('|')
                elif self.plane[(x, y)] == self.NS_DOOR:
                    sys.stdout.write('-')
                elif self.plane[(x, y)] == self.EMPTY_ROOM:
                    sys.stdout.write('.')
                elif self.plane[(x, y)] == self.START:
                    sys.stdout.write('X')
            sys.stdout.write('\n')

    def all_traveled(self):
        for value in self.routes:
            if not value.traveled:
                return False
        return True

    def next_untraveled(self):
        for route in self.routes:
            if not route.traveled:
                return route.route_index

    def adjust_minmax(self, x, y):
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def create_map(self):
        x = self.curr_pos_x
        y = self.curr_pos_y

        start_point = self.routes[0]
        num_doors = start_point.total_doors
        while True:
            #print(start_point.route_str)
            start_point.start_x = x
            start_point.start_y = y
            #print("starting (%d, %d)" % (x, y))
            for direction in start_point.route_str:
                prev_x = x
                prev_y = y
                if 'E' == direction:
                    self.plane[(x+1, y)] = self.EW_DOOR
                    self.plane[(x+2, y)] = self.EMPTY_ROOM
                    x += 2
                elif 'W' == direction:
                    self.plane[(x-1, y)] = self.EW_DOOR
                    self.plane[(x-2, y)] = self.EMPTY_ROOM
                    x -= 2
                elif 'S' == direction:
                    self.plane[(x, y+1)] = self.NS_DOOR
                    self.plane[(x, y+2)] = self.EMPTY_ROOM
                    y += 2
                elif 'N' == direction:
                    self.plane[(x, y-1)] = self.NS_DOOR
                    self.plane[(x, y-2)] = self.EMPTY_ROOM
                    y -= 2
                num_doors += 1
                self.adjust_minmax(x, y)
                self.rooms.append((x, y, num_doors))
                if self.room_plane[(x, y)] != 0:
                    self.room_plane[(x, y)] = min(self.room_plane[(x, y)], self.room_plane[(prev_x, prev_y)] + 1)
                else:
                    self.room_plane[(x, y)] = self.room_plane[(prev_x, prev_y)] + 1
            start_point.finish_x = x
            start_point.finish_y = y
            start_point.traveled = True
            if self.all_traveled():
                break
            start_point = self.routes[self.next_untraveled()]
            x = self.routes[start_point.parent].finish_x
            y = self.routes[start_point.parent].finish_y

    def find_most_rooms(self):
        self.rooms.sort(key=lambda x: x[2], reverse=True)
        return np.amax(self.room_plane)
        #return self.rooms[0][2]

    def find_greater(self, num):
        num_greater = 0
        return (self.room_plane >= 1000).sum()

class MapRoute(object):
    def __init__(self, node_data, route_index):
        self.route_str = ''.join(node_data)
        self.route_index = route_index
        self.options = []
        self.options_str = []
        self.traveled = False
        self.travel_count = 0
        self.parent = None
        self.start_x = 0
        self.start_y = 0
        self.finish_x = 0
        self.finish_y = 0
        self.total_doors = 0

    def add_option(self, option_str, option_index):
        self.options_str.append(option_str)
        self.options.append(option_index)


def solve_p1(routes):
    elf_map = RegularMap(routes)
    elf_map.create_map()
    elf_map.print_map()
    print("PART1: %d" % elf_map.find_most_rooms())


def solve_p2(routes):
    elf_map = RegularMap(routes)
    elf_map.create_map()
    elf_map.print_map()
    print("PART2: %d" % elf_map.find_greater(1000))


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()
    #print(data_list[0])

    # Check if all optional routes end up back at same place
    checking_all = False

    data_str = data_list[0][1:]

    if False:
        match = re.findall(r"\([WSNE]+\|\)", data_str)
        if match:
            for m in match:
                data_str = data_str.replace(m, '')

            if checking_all:
                items = defaultdict(list)
                for m in match:
                    m = m.strip('\)').strip('\(').strip('\|')
                    for s in m:
                        items[s].append(s)
                if not(len(items['W']) == len(items['E']) and
                   len(items['S']) == len(items['N'])):
                    print("here")
    #print(data_str)

    node_data = []
    routes = []
    route_index = 0
    prev_x = prev_y = x = y = 0
    dists = defaultdict(int)
    stack = []
    curr_parent = []
    for i in range(0, len(data_str)):
        if data_str[i] == '$':
            if len(routes) == 0:
                new_node = MapRoute(node_data, route_index)
                new_node.parent = 0
                routes.append(new_node)
            break

        if data_str[i] == '(':
            stack.append((x, y))
            new_node = MapRoute(node_data, route_index)
            if len(curr_parent) == 0:
                new_node.parent = 0
            else:
                new_node.parent = curr_parent[-1]
            route_index += 1
            routes.append(new_node)
            #if route_index > 1:
            if len(curr_parent):
                routes[curr_parent[-1]].add_option(new_node.route_str, new_node.route_index)
            curr_parent.append(new_node.route_index)
            node_data = []
        elif data_str[i] == '|':
            #if data_str[i - 1] != ')':
            x, y = stack[-1]
            new_node = MapRoute(node_data, route_index)
            new_node.parent = curr_parent[-1]
            route_index += 1
            routes.append(new_node)
            node_data = []
            routes[curr_parent[-1]].add_option(new_node.route_str, new_node.route_index)
        elif data_str[i] == ')':
            new_node = MapRoute(node_data, route_index)
            new_node.parent = curr_parent[-1]
            route_index += 1
            routes.append(new_node)
            node_data = []
            routes[curr_parent.pop()].add_option(new_node.route_str, new_node.route_index)
            x, y = stack.pop()
        else:
            node_data.append(data_str[i])
            if 'E' == data_str[i]:
                x += 1
            elif 'W' == data_str[i]:
                x -= 1
            elif 'S' == data_str[i]:
                y += 1
            elif 'N' == data_str[i]:
                y -= 1
            if dists[(x, y)] != 0:
                dists[(x, y)] = min(dists[(x, y)], dists[(prev_x, prev_y)] + 1)
            else:
                dists[(x, y)] = dists[(prev_x, prev_y)] + 1
        prev_x = x
        prev_y = y
    print("PART1: %d" % max(dists.values()))
    print("PART2: %d" % len([i for i in dists.values() if i >= 1000]))

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
