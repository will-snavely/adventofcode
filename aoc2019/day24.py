test_inputs = [
    "inputs/day24"
]

deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def adj(grid, r, c):
    result = []
    for direction, delta in enumerate(deltas):
        rt = r + delta[0]
        ct = c + delta[1]
        if 0 <= rt < len(grid) and 0 <= ct < len(grid[rt]):
            result.append((rt, ct))
    return result


def step_part1(grid):
    result = []
    for r, line in enumerate(grid):
        row = ""
        for c, char in enumerate(line):
            neighbors = adj(grid, r, c)
            bugs = len([p for p in neighbors if grid[p[0]][p[1]] == "#"])
            if char == "#":
                if bugs != 1:
                    row += "."
                else:
                    row += "#"
            else:
                if bugs == 1 or bugs == 2:
                    row += "#"
                else:
                    row += "."
        result.append(row)
    return result


def score(grid):
    result = 0
    power = 1
    for row in grid:
        for char in row:
            if char == "#":
                result += power
            power *= 2
    return result


def draw(grid):
    for line in grid:
        print(line)


def part1(grid):
    seen = set()
    while True:
        biodiversity = score(grid)
        if biodiversity in seen:
            return biodiversity
        seen.add(biodiversity)
        grid = step_part1(grid)


def adj_recursive(coord):
    level, r, c = coord
    for direction, delta in enumerate(deltas):
        rt = r + delta[0]
        ct = c + delta[1]
        if rt == -1:
            yield level - 1, 1, 2
        elif ct == -1:
            yield level - 1, 2, 1
        elif rt == 5:
            yield level - 1, 3, 2
        elif ct == 5:
            yield level - 1, 2, 3
        elif rt == 2 and ct == 2:
            if direction == 0:
                for x in range(5):
                    yield level + 1, 0, x
            elif direction == 1:
                for x in range(5):
                    yield level + 1, x, 0
            elif direction == 2:
                for x in range(5):
                    yield level + 1, 4, x
            elif direction == 3:
                for x in range(5):
                    yield level + 1, x, 4
        else:
            yield level, rt, ct


def step_part2(bugs):
    closure = set()
    closure = closure | bugs
    for bug in bugs:
        closure = closure | set(adj_recursive(bug))

    result = set()
    for point in closure:
        bug_count = len([p for p in adj_recursive(point) if p in bugs])
        if point in bugs:
            if bug_count == 1:
                result.add(point)
        else:
            if bug_count == 1 or bug_count == 2:
                result.add(point)
    return result


def draw_recursive(bugs):
    levels = [p[0] for p in bugs]
    for lvl in range(min(levels), max(levels) + 1):
        print("Level", lvl)
        for r in range(5):
            line = ""
            for c in range(5):
                if (lvl, r, c) in bugs:
                    line += "#"
                else:
                    line += "."
            print(line)


def part2(grid):
    bugs = set()
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == "#":
                bugs.add((0, r, c))

    for _ in range(200):
        bugs = step_part2(bugs)
    return len(bugs)


def process(path):
    with open(path) as f:
        grid = [line.strip() for line in f.readlines()]
    print(part1(grid))
    print(part2(grid))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
