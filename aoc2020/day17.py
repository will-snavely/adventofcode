test_inputs = [
    "inputs/day17_sample",
    "inputs/day17_test1"
]


class World4d:
    def __init__(self, active=None):
        self.active = set()
        if active:
            self.active = active

    def adjacent(self, coord):
        x, y, z, w = coord
        for wp in range(w - 1, w + 2):
            for zp in range(z - 1, z + 2):
                for yp in range(y - 1, y + 2):
                    for xp in range(x - 1, x + 2):
                        if zp == z and yp == y and xp == x and wp == w:
                            continue
                        yield xp, yp, zp, wp

    def iterate(self):
        workset = set()
        workset = workset.union(self.active)
        for point in self.active:
            for adj in self.adjacent(point):
                workset.add(adj)

        active_next = set()
        for point in workset:
            active_neighbors = len([adj for adj in self.adjacent(point) if adj in self.active])
            if point in self.active:
                if active_neighbors in [2, 3]:
                    active_next.add(point)
            else:
                if active_neighbors == 3:
                    active_next.add(point)

        return World4d(active=active_next)


class World3d:
    def __init__(self, active=None):
        self.active = set()
        if active:
            self.active = active

    def adjacent(self, coord):
        x, y, z = coord
        for zp in range(z - 1, z + 2):
            for yp in range(y - 1, y + 2):
                for xp in range(x - 1, x + 2):
                    if zp == z and yp == y and xp == x:
                        continue
                    yield xp, yp, zp

    def iterate(self):
        workset = set()
        workset = workset.union(self.active)
        for point in self.active:
            for adj in self.adjacent(point):
                workset.add(adj)

        active_next = set()
        for point in workset:
            active_neighbors = len([adj for adj in self.adjacent(point) if adj in self.active])
            if point in self.active:
                if active_neighbors in [2, 3]:
                    active_next.add(point)
            else:
                if active_neighbors == 3:
                    active_next.add(point)

        return World3d(active=active_next)


def process(path):
    print("Input:", path)
    text_grid = []
    with open(path) as f:
        for line in f:
            text_grid.append(line.strip())

    world3d = World3d()
    world4d = World4d()
    for row in range(len(text_grid)):
        for col in range(len(text_grid[row])):
            if text_grid[row][col] == "#":
                world3d.active.add((row, col, 0))
                world4d.active.add((row, col, 0, 0))

    iter_count = 6
    while iter_count > 0:
        world3d = world3d.iterate()
        iter_count -= 1
    print(len(world3d.active))

    iter_count = 6
    while iter_count > 0:
        world4d = world4d.iterate()
        iter_count -= 1
    print(len(world4d.active))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
