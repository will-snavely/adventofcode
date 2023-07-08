import itertools

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def __getitem__(self, key):
        return self.grid[key]

    def __repr__(self):
        return repr(self.grid)

    def __str__(self):
        s = ""
        for row in self.grid:
            s += str(row) + ",\n"
        return s

    def __iter__(self):
        return itertools.chain.from_iterable(self.grid)

    def walk(self, start_row, start_col, dr, dc):
        row = start_row
        col = start_col
        while row >= 0 and col >= 0 and row < self.rows and col < self.cols:
            yield (row, col, self.grid[row][col])
            row += dr
            col += dc

class Tree:
    def __init__(self, height, visible=False):
        self.visible = visible
        self.height = height
        self.score = 0

    def __repr__(self):
        return "Tree({}, {})".format(self.height, self.visible)

def find_visible(grid, start_row, start_col, dr, dc):
    max_height = -1
    for (row, col, tree) in grid.walk(start_row, start_col, dr, dc):
        if tree.height > max_height:
            max_height = tree.height
            yield tree

def view(grid, start_row, start_col, dr, dc):
    init_height = grid[start_row][start_col].height
    for (r, c, tree) in grid.walk(start_row + dr, start_col + dc, dr, dc):
        yield tree
        if tree.height >= init_height:
            break

def view_distance(grid, start_row, start_col, dr, dc):
    return sum(1 for _ in view(grid, start_row, start_col, dr, dc))

def scenic_score(grid, row, col):
    result = 1
    for dr in [1,-1]:
        result *= view_distance(grid, row, col, dr, 0)
    for dc in [1,-1]:
        result *= view_distance(grid, row, col, 0, dc)
    return result

if __name__ == "__main__":
    with open("inputs/day08") as f:
        lines = [line.strip() for line in f]
        grid = Grid(len(lines), len(lines[0]))
        row = 0
        for line in lines:
            for col in range(len(line.strip())):
                grid[row][col] = Tree(int(line[col]))
            row += 1

        for row in range(0, grid.rows):
            for tree in find_visible(grid, row, 0, 0, 1):
                tree.visible = True
            for tree in find_visible(grid, row, grid.cols - 1, 0, -1):
                tree.visible = True
        for col in range(0, grid.cols - 1):
            for tree in find_visible(grid, 0, col, 1, 0):
                tree.visible = True
            for tree in find_visible(grid, grid.rows - 1, col, -1, 0):
                tree.visible = True

        print(sum(1 for tree in grid if tree.visible))

        for row in range(1, grid.rows - 1):
            for col in range(1, grid.cols - 1):
                grid[row][col].score = scenic_score(grid, row, col)
        print(max(tree.score for tree in grid))


