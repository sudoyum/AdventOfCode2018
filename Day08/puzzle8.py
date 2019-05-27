import os
import sys


PARSE_NODE = 0
PARSE_METADATA = 1
PARSE_METADATA_NOC = 2


class Node(object):
    def __init__(self, num_c, num_m, parent_id, id):
        self.num_c = num_c
        self.num_m = num_m
        self.metadata = []
        self.resolved_children = 0
        self.parent_id = parent_id
        self.id = id
        self.total_value = -1
        self.children = {}
        self.c_index = 1

    def add_metadata(self, metadata):
        self.metadata += metadata

    def is_resolved(self):
        if len(self.metadata) == self.num_m and self.resolved_children == self.num_c:
            return True
        return False

    def is_c_resolved(self):
        if self.resolved_children == int(self.num_c):
            return True
        return False

    def set_id(self, id):
        self.id = id

    def child_resolved(self, child):
        self.resolved_children += 1
        if child != self.id:
            self.children[self.c_index] = child
            self.c_index += 1

    def set_node_value(self, total_value):
        self.total_value = total_value


def solve_p1_p2(data):
    tree = {}
    state = PARSE_NODE
    current_id = 0
    parent_id = 0
    data = data[::-1]
    root = Node(int(data.pop()), int(data.pop()), 0, 0)
    tree[0] = root
    while data:
        if state == PARSE_NODE:
            num_c = int(data.pop())
            num_m = int(data.pop())
            if num_m == 0:
                sys.exit(1)
            current_id += 1
            tree[current_id] = Node(num_c, num_m, parent_id, current_id)
            temp_id = current_id
            if num_c == 0:
                state = PARSE_METADATA_NOC
            else:
                parent_id = current_id

        if state == PARSE_METADATA_NOC:
            metadata = []
            if num_m == 0:
                sys.exit(1)
            while int(num_m) > 0:
                metadata.append(data.pop())
                num_m -= 1
            if metadata:
                tree[temp_id].add_metadata(metadata)
                tree[parent_id].child_resolved(temp_id)
                if not tree[tree[temp_id].parent_id].is_c_resolved():
                    state = PARSE_NODE
                else:
                    temp_id = tree[temp_id].parent_id
                    parent_id = tree[temp_id].parent_id
                    num_m = int(tree[temp_id].num_m)
    total_metadata = 0
    for values in tree.values():
        for metadata in values.metadata:
            total_metadata += int(metadata)

    print("PART1: %d" % total_metadata)

    for key, value in tree.items():
        if value.num_c == 0:
            total_metadata = 0
            for metadata in value.metadata:
                total_metadata += int(metadata)
            tree[key].set_node_value(total_metadata)

    not_done = True
    while not_done:
        for key, value in tree.items():
            total_metadata = 0
            is_set = True
            if tree[key].num_c > 0:
                for metadata in tree[key].metadata:
                    if int(metadata) in tree[key].children.keys():
                        index = tree[key].children[int(metadata)]
                        if tree[index].total_value == -1:
                            is_set = False
                            break
                        else:
                            total_metadata += tree[index].total_value
            if is_set:
                if tree[key].total_value == -1:
                    tree[key].total_value = total_metadata

        not_done = False
        for key, value in tree.items():
            if tree[key].total_value == -1:
                not_done = True
                break
    print("PART2: %d" % tree[0].total_value)


def format_input(f_name):
    with open(f_name, "r") as file:
        data_list = file.read().splitlines()

    data = []
    for line in data_list:
        data += line.strip('\n').split(" ")
    solve_p1_p2(data)


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