test_inputs = [
    "inputs/day23"
]


class Node:
    def __init__(self, value, nxt=None):
        self.v = value
        self.n = nxt


def step(cups):
    index_map = {}
    for idx, val in enumerate(cups):
        index_map[val] = idx

    current = cups[0]
    to_move = cups[1:4]
    destination = current - 1
    if destination == 0:
        destination = len(cups)
    while destination in to_move:
        destination = (destination - 1)
        if destination == 0:
            destination = len(cups)

    destination_idx = index_map[destination]
    next_cups = []
    for idx in range(4, len(cups)):
        next_cups.append(cups[idx])
        if idx == destination_idx:
            next_cups += to_move
    next_cups.append(current)
    return next_cups


def step2(node_map, cur, size):
    cur_node = node_map[cur]
    first_to_move = cur_node.n
    last_to_move = cur_node.n.n.n
    move_values = {cur_node.n.v, cur_node.n.n.v, cur_node.n.n.n.v}
    dest = cur_node.v
    while True:
        dest = dest - 1
        if dest == 0:
            dest = size
        if dest not in move_values:
            break
    dest_node = node_map[dest]

    cur_node.n = last_to_move.n
    tmp = dest_node.n
    dest_node.n = first_to_move
    last_to_move.n = tmp
    return cur_node.n.v


def process(path):
    print("Input:", path)

    with open(path) as f:
        for line in f:
            cups = [int(c) for c in line.strip()]
            node_map = {}
            prev = None
            for cup in cups + list(range(len(cups) + 1, 10 ** 6 + 1)):
                node_map[cup] = Node(cup)
                if prev:
                    prev.n = node_map[cup]
                prev = node_map[cup]
            prev.n = node_map[cups[0]]

            cur = cups[0]
            for x in range(10 ** 7):
                cur = step2(node_map, cur, 10 ** 6)

            one_node = node_map[1]
            print(one_node.n.v * one_node.n.n.v)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
