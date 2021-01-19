import collections
import string

test_inputs = [
    "inputs/day18_part1"
]

deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_maze(lines):
    maze = {}
    entrances = list()
    doors = set()
    keys = set()
    for r, line in enumerate(lines):
        for c, v in enumerate(line.strip()):
            if v in string.ascii_lowercase:
                keys.add((r, c))
            elif v in string.ascii_uppercase:
                doors.add((r, c))
            elif v == "@":
                entrances.append((r, c))

            maze[(r, c)] = v
    return maze, entrances, doors, keys


def draw_maze(maze):
    points = maze.keys()
    rows = [p[0] for p in points]
    cols = [p[1] for p in points]
    for r in range(0, max(rows) + 1):
        line = ""
        for c in range(0, max(cols) + 1):
            line += maze[(r, c)]
        print(line)


def adj(maze, point):
    result = []
    for direction, delta in enumerate(deltas):
        p = (point[0] + delta[0], point[1] + delta[1])
        if p in maze and maze[p] != "#":
            result.append((direction, p))
    return result


def bfs(maze, position, doors, keys):
    queue = collections.deque()
    queue.append((position, 0))
    visited = set()
    reachable_keys = set()
    while queue:
        pos, depth = queue.popleft()
        visited.add(pos)
        if pos in keys:
            reachable_keys.add((pos, depth))
        elif pos not in doors:
            for direction, neighbor in adj(maze, pos):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
    return reachable_keys


memo_count = 0


def explore(maze, positions, doors, keys, memo):
    global memo_count
    if len(keys) == 0:
        return 0

    door_str = "".join(sorted([maze[p] for p in doors]))
    key_str = "".join(sorted([maze[p] for p in keys]))
    state = (tuple(positions), door_str, key_str)
    if state in memo:
        memo_count += 1
        return memo[state]

    all_reachable_keys = collections.defaultdict(set)
    for index, start in enumerate(positions):
        reachable_keys = bfs(maze, start, doors, keys)
        all_reachable_keys[index] = reachable_keys

    options = []
    for index, reachable in all_reachable_keys.items():
        for key_pos, dist in reachable:
            key = maze[key_pos]
            door_pos = set([p for p in doors if maze[p] == key.upper()])
            rec_doors = doors - door_pos
            rec_keys = keys - {key_pos}
            rec_positions = positions.copy()
            rec_positions[index] = key_pos
            rec_dist = explore(maze, rec_positions, rec_doors, rec_keys, memo)
            options.append(dist + rec_dist)

    memo[state] = min(options)
    return memo[state]


def part1():
    global memo_count
    memo_count = 0
    with open("inputs/day18_part1") as f:
        lines = f.readlines()
        maze, entrances, doors, keys = parse_maze(lines)
        print(explore(maze, entrances, doors, keys, {}))


def part2():
    global memo_count
    memo_count = 0
    with open("inputs/day18_part2") as f:
        lines = f.readlines()
        maze, entrances, doors, keys = parse_maze(lines)
        print(explore(maze, list(entrances), doors, keys, {}))


def main():
    part1()
    part2()


if __name__ == "__main__":
    main()
