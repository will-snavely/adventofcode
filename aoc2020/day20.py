import collections
import math

test_inputs = [
    "inputs/day20",
    "inputs/day20_sample"
]
sea_monster = """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
"""


class Transform:
    def __init__(self, rot, flip):
        self.rot = rot
        self.flip = flip


def monster_offsets():
    lines = [line for line in sea_monster.split("\n") if line.strip() != ""]
    result = set()
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "#":
                result.add((r, c))
    return result


class ImageTile:
    def __init__(self, tile_id, grid):
        self.id = tile_id
        self.grid = grid

    def __getitem__(self, item):
        return self.grid[item]

    def match(self, r, c, offsets):
        matches = set()
        for rd, cd in offsets:
            rf = r + rd
            cf = c + cd
            if rf < len(self.grid) and cf < len(self.grid[rf]):
                if self.grid[rf][cf] not in ("#", "O"):
                    return False
                else:
                    matches.add((rf, cf))
            else:
                return False
        return matches

    def count_hashes(self):
        count = 0
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                if self.grid[r][c] == "#":
                    count += 1
        return count

    def find_monsters(self):
        offsets = monster_offsets()
        hits = set()
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                matches = self.match(r, c, offsets)
                if matches:
                    hits = hits.union(matches)
        return hits

    def flip_x(self):
        new_grid = [[None for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]
        for r in range(len(new_grid)):
            for c in range(len(new_grid[r])):
                new_grid[r][c] = self.grid[r][len(new_grid[r]) - c - 1]
        return ImageTile(self.id, new_grid)

    def rot(self):
        rc = len(self.grid)
        cc = len(self.grid[0])
        new_grid = [[None for _ in range(cc)] for _ in range(rc)]
        for r in range(len(new_grid)):
            for c in range(len(new_grid[r])):
                new_grid[r][c] = self.grid[rc - c - 1][r]
        return ImageTile(self.id, new_grid)

    def transform(self, tform):
        result = self
        if tform.flip:
            result = result.flip_x()
        for _ in range(tform.rot):
            result = result.rot()
        return result

    def __str__(self):
        result = ""
        for r in range(len(self.grid)):
            result += "".join(self.grid[r]) + "\n"
        return result


class TileEdges:
    def __init__(self, tile_id, edges):
        self.id = tile_id
        self.edges = edges.copy()

    @staticmethod
    def from_grid(tile_id, grid):
        edges = [
            tuple(grid[0]),
            tuple([grid[i][-1] for i in range(len(grid))]),
            tuple(reversed(grid[-1])),
            tuple([grid[i][0] for i in range(len(grid) - 1, -1, -1)])
        ]
        return TileEdges(tile_id, edges)

    def flip_x(self):
        new_edges = [
            tuple(reversed(self.edges[i]))
            for i in [0, 3, 2, 1]
        ]
        return TileEdges(self.id, new_edges)

    def rot(self):
        new_edges = []
        for idx in range(4):
            new_edges.append(self.edges[(idx - 1) % 4])
        return TileEdges(self.id, new_edges)

    def perms(self):
        cur = self
        flipped = False
        for f in range(2):
            for r in range(4):
                yield cur, Transform(rot=r, flip=flipped)
                cur = cur.rot()
            cur = self.flip_x()
            flipped = True


def put_together(
        tile_map,
        available_tiles,
        grid,
        row,
        col):
    if row >= len(grid):
        return True

    above = None
    below = None
    left = None
    right = None
    if row - 1 >= 0:
        above = grid[row - 1][col]
    if row + 1 < len(grid):
        below = grid[row + 1][col]
    if col - 1 >= 0:
        left = grid[row][col - 1]
    if col + 1 < len(grid[row]):
        right = grid[row][col + 1]

    nc = col + 1
    nr = row
    if nc == len(grid[row]):
        nc = 0
        nr += 1

    for tile_id in available_tiles:
        tile = tile_map[tile_id]
        for perm, tform in tile.perms():
            fits = True
            if above:
                fits = fits and perm.edges[0] == tuple(reversed(above[0].edges[2]))
            if fits and below:
                fits = fits and perm.edges[2] == tuple(reversed(below[0].edges[0]))
            if fits and left:
                fits = fits and perm.edges[3] == tuple(reversed(left[0].edges[1]))
            if fits and right:
                fits = fits and perm.edges[1] == tuple(reversed(right[1].edges[3]))
            if fits:
                grid[row][col] = (perm, tform)
                rec = put_together(tile_map, available_tiles - {tile_id}, grid, nr, nc)
                if rec:
                    return True
                grid[row][col] = None
    return False


def parse_raw_tiles(path):
    result = collections.defaultdict(list)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Tile"):
                parts = line.strip().strip(":").split()
                id = int(parts[1])
            else:
                result[id].append(list(line.strip()))
    return result


def process(path):
    print("Input:", path)
    monster_offsets()
    tile_map = {}
    orig_grids = {}
    for tid, grid in parse_raw_tiles(path).items():
        tile_map[tid] = TileEdges.from_grid(tid, grid)
        orig_grids[tid] = grid
        tile_size = len(tile_map[tid].edges[0]) - 2
    side_len = int(math.sqrt(len(tile_map)))
    puzzle_grid = [[None for _ in range(side_len)] for _ in range(side_len)]
    if put_together(tile_map, set(tile_map.keys()), puzzle_grid, 0, 0):
        print("Part 1: ",
              puzzle_grid[0][0][0].id
              * puzzle_grid[0][-1][0].id
              * puzzle_grid[-1][0][0].id
              * puzzle_grid[-1][-1][0].id)

        image_size = side_len * tile_size
        image = [[None for _ in range(image_size)] for _ in range(image_size)]
        for row in range(side_len):
            for col in range(side_len):
                tile, tform = puzzle_grid[row][col]
                image_tile = ImageTile(tile.id, orig_grids[tile.id]).transform(tform)
                for r in range(tile_size):
                    for c in range(tile_size):
                        image[row * tile_size + r][col * tile_size + c] = image_tile[r + 1][c + 1]

        final_image = ImageTile(0, image)
        for _ in range(2):
            for _ in range(4):
                hits = final_image.find_monsters()
                for r, c in hits:
                    final_image[r][c] = "O"
                final_image = final_image.rot()
            final_image = final_image.flip_x()

        print("Part 2:", final_image.count_hashes())


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
