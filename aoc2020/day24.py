import collections

test_inputs = [
    "inputs/day24_sample",
    "inputs/day24"
]


def parse_directions(s):
    stack = []
    for c in s.strip():
        if c in ["e", "w"]:
            if stack:
                yield stack.pop() + c
            else:
                yield c
        elif c in ["n", "s"]:
            stack.append(c)


def traverse(directions):
    x = y = 0
    counts = collections.Counter(directions)
    x += 2 * counts["e"] + counts["ne"] + counts["se"]
    x -= 2 * counts["w"] + counts["nw"] + counts["sw"]
    y += (counts["ne"] + counts["nw"])
    y -= (counts["se"] + counts["sw"])
    return x, y


def adj(p):
    yield p[0] + 2, p[1]
    yield p[0] - 2, p[1]
    yield p[0] + 1, p[1] + 1
    yield p[0] - 1, p[1] + 1
    yield p[0] + 1, p[1] - 1
    yield p[0] - 1, p[1] - 1


def round(black_tiles: set):
    points_to_consider = set()
    points_to_consider = points_to_consider | black_tiles
    for point in black_tiles:
        for n in adj(point):
            points_to_consider.add(n)

    made_black = set()
    made_white = set()
    for point in points_to_consider:
        is_black = point in black_tiles
        black_neighbors = len(set(adj(point)) & black_tiles)
        if is_black:
            if black_neighbors == 0 or black_neighbors > 2:
                made_white.add(point)
        else:
            if black_neighbors == 2:
                made_black.add(point)

    return (black_tiles - made_white) | made_black


def process(path):
    print("Input:", path)

    with open(path) as f:
        points = [traverse(parse_directions(line)) for line in f]
        counts = collections.Counter(points)
        black_tiles = [p for p in points if counts[p] % 2 == 1]
        print("\tPart 1:", len(black_tiles))
        for _ in range(100):
            black_tiles = round(set(black_tiles))
        print("\tPart 2:", len(black_tiles))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
