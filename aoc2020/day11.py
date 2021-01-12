test_inputs = [
    "inputs/day11_sample",
    "inputs/day11"
]


class SeatWorld:
    def __init__(self):
        self.grid = []

    def add_row(self, row):
        self.grid.append(row)

    def in_bounds(self, row, col):
        return 0 <= row < len(self.grid) and 0 <= col < len(self.grid[row])

    def get_immediate_adjacent(self, row, col):
        points = [
            (row, col - 1),
            (row, col + 1),
            (row - 1, col),
            (row - 1, col + 1),
            (row - 1, col - 1),
            (row + 1, col),
            (row + 1, col + 1),
            (row + 1, col - 1),
        ]

        return [(r, c) for r, c in points if self.in_bounds(r, c)]

    def get_nearest(self, row, col):
        result = []
        deltas = [
            (1, 0), (1, 1), (1, -1),
            (-1, 0), (-1, 1), (-1, -1),
            (0, 1), (0, -1)
        ]

        for delta in deltas:
            dr, dc = delta
            r = row + dr
            c = col + dc
            while self.in_bounds(r, c):
                if self.grid[r][c] != ".":
                    result.append((r, c))
                    break
                r += dr
                c += dc

        return result

    def step(self, adjacent_func, leave_threshold):
        next_world = SeatWorld()
        for r in range(0, len(self.grid)):
            next_row = ""
            for c in range(0, len(self.grid[r])):
                seat = self.grid[r][c]
                adjacent = [self.grid[x][y] for x, y in adjacent_func(r, c)]
                occupied_count = len([s for s in adjacent if s == "#"])
                next_state = seat
                if seat == "L":
                    if occupied_count == 0:
                        next_state = "#"
                elif seat == "#":
                    if occupied_count >= leave_threshold:
                        next_state = "L"
                next_row += next_state
            next_world.add_row(next_row)
        return next_world

    def print(self):
        for row in self.grid:
            print(row)

    def seats(self):
        for r in range(0, len(self.grid)):
            for c in range(0, len(self.grid[r])):
                yield self.grid[r][c]


def part1_fixpoint(world):
    while True:
        next_world = world.step(world.get_immediate_adjacent, 4)
        if next_world.grid == world.grid:
            occupied = len([seat for seat in world.seats() if seat == "#"])
            print("\tPart 1:", occupied)
            break
        world = next_world


def part2_fixpoint(world):
    while True:
        next_world = world.step(world.get_nearest, 5)
        if next_world.grid == world.grid:
            occupied = len([seat for seat in world.seats() if seat == "#"])
            print("\tPart 2:", occupied)
            break
        world = next_world


def process(path):
    print("Input:", path)
    with open(path) as f:
        world = SeatWorld()
        for line in f:
            world.add_row(line.strip())
        part1_fixpoint(world)
        part2_fixpoint(world)
        """
        world_part2 = world
        while True:
            next_world = world_part2.step(world_part2.get_nearest)
            if next_world.grid == world.grid:
                occupied = len([seat for seat in world.seats() if seat == "#"])
                print("\tOccupied:", occupied)
                break
            world_part2 = next_world
        """


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
