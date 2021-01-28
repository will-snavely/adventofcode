import pyparsing as pp

Integer = pp.Word(pp.nums).setParseAction(pp.tokenMap(int))
Axis = pp.Word("xy")
Range = (Integer + pp.Suppress("..") + Integer)
Value = Integer ^ Range
Constraint = pp.Group(Axis("axis") + pp.Suppress("=") + Value("value"))
Line = Constraint + pp.Suppress(",") + Constraint


class World:
    def __init__(self):
        self.grid = {}
        self.spring = (0, 500)
        self.max_row = None
        self.min_row = None

    def draw(self):
        points = self.grid.keys()
        rows = [p[0] for p in points]
        cols = [p[1] for p in points]
        max_row = max(rows)
        min_col, max_col = min(cols), max(cols)
        for row in range(0, max_row + 1):
            line = ""
            for col in range(min_col, max_col + 1):
                if (row, col) in self.grid:
                    line += self.grid.get((row, col))
                else:
                    line += "."
            print(line)

    def flow(self, start):
        if self.grid.get(start) in set("#~"):
            return
        bottom = start
        while True:
            if bottom[0] > self.max_row:
                return
            self.grid[bottom] = "|"
            below = (bottom[0] + 1, bottom[1])
            if self.grid.get(below) in set("#~"):
                break
            bottom = below

        left_bound = bottom
        left_wall = False
        while True:
            self.grid[left_bound] = "|"
            below = (left_bound[0] + 1, left_bound[1])
            left = (left_bound[0], left_bound[1] - 1)
            if self.grid.get(left) in set("#~"):
                left_wall = True
                break
            elif self.grid.get(below) not in set("#~"):
                break
            left_bound = left

        right_bound = bottom
        right_wall = False
        while True:
            self.grid[right_bound] = "|"
            below = (right_bound[0] + 1, right_bound[1])
            right = (right_bound[0], right_bound[1] + 1)
            if self.grid.get(right) in set("#~"):
                right_wall = True
                break
            elif self.grid.get(below) not in set("#~"):
                break
            right_bound = right

        if left_wall and right_wall:
            row = bottom[0]
            for col in range(left_bound[1], right_bound[1] + 1):
                self.grid[(row, col)] = "~"
        else:
            if not left_wall:
                self.flow(left_bound)
            if not right_wall:
                self.flow(right_bound)

    def count(self, matching=None):
        if matching is None:
            matching = set("~|")
        return len([
            p for p in self.grid
            if self.grid.get(p) in matching and self.min_row <= p[0] <= self.max_row
        ])


def build_world(path):
    world = World()
    with open(path) as f:
        for line in f:
            parsed = Line.parseString(line)
            limits = {}
            for constraint in parsed:
                limits[constraint["axis"]] = list(constraint["value"])
            for col in range(limits["x"][0], limits["x"][-1] + 1):
                for row in range(limits["y"][0], limits["y"][-1] + 1):
                    world.grid[(row, col)] = "#"
    rows = [p[0] for p in world.grid]
    world.min_row = min(rows)
    world.max_row = max(rows)
    return world


def main():
    tests = [
        "inputs/day17"
    ]
    for path in tests:
        print("Input:", path)
        world = build_world(path)
        count = world.count()
        while True:
            world.flow((0, 500))
            update = world.count()
            if update == count:
                break
            count = update
        print("\tPart 1:", count)
        print("\tPart 2:", world.count(matching=set("~")))


if __name__ == "__main__":
    main()
