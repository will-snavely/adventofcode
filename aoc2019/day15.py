import collections

from aoc2019.intcode import IntCodeProcess

test_inputs = [
    "inputs/day15_test1"
]

delta = {
    1: (0, 1),
    2: (0, -1),
    3: (1, 0),
    4: (-1, 0)
}

inverse = {
    1: 2,
    2: 1,
    3: 4,
    4: 3
}


class MapNode:
    def __init__(self, type, position):
        self.type = type
        self.position = position


def move(controller: IntCodeProcess, command):
    controller.send(command)
    controller.run()
    output = controller.flush()
    return output[0]


def explore(
        position,
        floor_map: dict,
        controller: IntCodeProcess,
        arrive_command):
    for command in [1, 2, 3, 4]:
        adj_position = (
            position[0] + delta[command][0],
            position[1] + delta[command][1]
        )
        if adj_position not in floor_map:
            result = move(controller, command)
            if result == 0:
                floor_map[adj_position] = "wall"
            elif result == 1:
                floor_map[adj_position] = "floor"
                explore(adj_position, floor_map, controller, command)
            elif result == 2:
                floor_map[adj_position] = "his"
                explore(adj_position, floor_map, controller, command)
    if arrive_command:
        move(controller, inverse[arrive_command])


def draw_map(floor_map):
    keys = list(floor_map.keys())
    xs = [k[0] for k in keys]
    ys = [k[1] for k in keys]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in floor_map:
                type = floor_map[(x, y)]
                if x == 0 and y == 0:
                    row += "S"
                elif type == "floor":
                    row += "."
                elif type == "wall":
                    row += "#"
                elif type == "his":
                    row += "$"
            else:
                row += "?"
        print(row)


def distances(floor_map, start):
    queue = collections.deque()
    queue.append((start, 0))
    result = {}
    while queue:
        cur, depth = queue.popleft()
        result[cur] = depth

        for dir in [1, 2, 3, 4]:
            adj = (cur[0] + delta[dir][0], cur[1] + delta[dir][1])
            if adj in floor_map and adj not in result:
                if floor_map[adj] != "wall":
                    queue.append((adj, depth + 1))
    return result


def solve(controller: IntCodeProcess):
    floor_map = {
        (0, 0): "floor"
    }
    explore((0, 0), floor_map, controller, None)
    draw_map(floor_map)
    o2_location = next(pos for pos in floor_map if floor_map[pos] == "his")
    distances_from_start = distances(floor_map, (0, 0))
    print(distances_from_start[o2_location])
    distances_from_o2 = distances(floor_map, o2_location)
    print(max(distances_from_o2.values()))


def main():
    for path in test_inputs:
        proc = IntCodeProcess.compile(path)
        solve(proc)


if __name__ == "__main__":
    main()
