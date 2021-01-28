import collections


def draw(grid):
    rs = [p[0] for p in grid]
    cs = [p[0] for p in grid]
    for r in range(0, max(rs) + 1):
        line = ""
        for c in range(0, max(cs) + 1):
            line += grid.get((r, c))
        print(line)


def step(grid):
    result = {}
    for p in grid:
        neighbors = []
        for r in range(-1, 2):
            for c in range(-1, 2):
                if r == 0 and c == 0:
                    continue
                adj = (p[0] + r, p[1] + c)
                if adj in grid:
                    neighbors.append(grid[adj])
        counts = collections.Counter(neighbors)
        if grid[p] == ".":
            result[p] = "."
            if counts["|"] >= 3:
                result[p] = "|"
        elif grid[p] == "|":
            result[p] = "|"
            if counts["#"] >= 3:
                result[p] = "#"
        elif grid[p] == "#":
            result[p] = "."
            if counts["#"] >= 1 and counts["|"] >= 1:
                result[p] = "#"
    return result


def parse(path):
    grid = {}
    with open(path) as f:
        for row, line in enumerate(f):
            for col, char in enumerate(line.strip()):
                grid[(row, col)] = char
    return grid


def part1(path):
    grid = parse(path)
    for _ in range(10):
        grid = step(grid)
    counts = collections.Counter(grid.values())
    score = counts["#"] * counts["|"]
    return score


def key(grid):
    return tuple([ord(grid[p]) for p in sorted(grid.keys())])


def part2(path):
    grid = parse(path)
    target = 1000000000
    cycle_start = 431
    cycle_end = 458
    cycle_len = cycle_end - cycle_start + 1
    offset = (target - cycle_start) % cycle_len
    for _ in range(cycle_start + offset):
        grid = step(grid)
    counts = collections.Counter(grid.values())
    score = counts["#"] * counts["|"]
    return score


def main():
    tests = [
        "inputs/day18"
    ]
    for path in tests:
        print(part1(path))
        print(part2(path))


if __name__ == "__main__":
    main()
