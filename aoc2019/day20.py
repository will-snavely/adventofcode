import collections
import string

test_inputs = [
    "inputs/day20"
]

deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def adj(grid, pos):
    result = []
    for direction, delta in enumerate(deltas):
        rt = pos[0] + delta[0]
        ct = pos[1] + delta[1]
        if 0 <= rt < len(grid) and 0 <= ct < len(grid[rt]):
            result.append((direction, rt, ct))
    return result


def parse_maze(lines):
    grid = []
    for line in lines:
        grid.append(line.strip("\n"))
    max_width = max(len(line) for line in grid)

    maze = {}
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == ".":
                maze[(row, col)] = []

    portals = collections.defaultdict(list)
    for pos in maze:
        for d, rt, ct in adj(grid, pos):
            char = grid[rt][ct]
            if char == ".":
                maze[pos].append(((rt, ct), "n"))
            elif char in string.ascii_uppercase:
                nc_row = rt + deltas[d][0]
                nc_col = ct + deltas[d][1]
                portal = char + grid[nc_row][nc_col]
                if d in [2, 3]:
                    portal = portal[::-1]
                kind = "i"
                if nc_row == 0 or nc_row == len(grid) - 1:
                    kind = "o"
                if nc_col == 0 or nc_col == max_width - 1:
                    kind = "o"
                portals[portal].append((pos, kind))

    for portal, points in portals.items():
        if len(points) == 2:
            maze[points[0][0]].append((points[1][0], points[0][1]))
            maze[points[1][0]].append((points[0][0], points[1][1]))
    return maze, portals["AA"][0][0], portals["ZZ"][0][0]


def bfs_part1(maze, start, end):
    queue = collections.deque()
    queue.append((start, 0))
    visited = set()
    while queue:
        pos, dist = queue.popleft()
        visited.add(pos)
        if pos == end:
            return dist
        for neighbor, _ in maze[pos]:
            if neighbor not in visited:
                queue.append((neighbor, dist + 1))
    return None


def bfs_part2(maze, start, end):
    queue = collections.deque()
    queue.append((start, 0, 0))
    visited = set()
    while queue:
        pos, dist, depth = queue.popleft()
        visited.add((pos, depth))
        if pos == end and depth == 0:
            return dist
        for neighbor, kind in maze[pos]:
            neighbor_depth = None
            if kind == "o" and depth > 0:
                neighbor_depth = depth - 1
            elif kind == "i":
                neighbor_depth = depth + 1
            elif kind == "n":
                neighbor_depth = depth
            if neighbor_depth is not None and (neighbor, neighbor_depth) not in visited:
                queue.append((neighbor, dist + 1, neighbor_depth))
    return None


def part1(path):
    with open(path) as f:
        lines = f.readlines()
        maze, start, end = parse_maze(lines)
        print(bfs_part1(maze, start, end))


def part2(path):
    with open(path) as f:
        lines = f.readlines()
        maze, start, end = parse_maze(lines)
        print(bfs_part2(maze, start, end))


def process(path):
    with open(path) as f:
        part1(path)
        part2(path)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
