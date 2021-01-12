import collections
import itertools
import math
from fractions import Fraction

test_inputs = [
    "inputs/day10"
]


def process(path):
    print("Input:", path)
    asteroids = []
    with open(path) as f:
        for row, line in enumerate(f):
            for col, val in enumerate(line):
                if val == "#":
                    asteroids.append((col, row))
        colinear = collections.defaultdict(set)
        for p1, p2 in itertools.combinations(asteroids, 2):
            x1, y1 = p1
            x2, y2 = p2
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0:
                colinear[(x1,)].add(p1)
                colinear[(x1,)].add(p2)
            else:
                m = Fraction(dy, dx)
                b = Fraction(y1) - m * Fraction(x1)
                colinear[(m, b)].add(p1)
                colinear[(m, b)].add(p2)

        counts = {}
        for ast in asteroids:
            counts[ast] = len(asteroids) - 1

        for key, value in colinear.items():
            line = sorted(list(value))
            for i, ast in enumerate(line):
                counts[ast] -= max(0, len(line) - (i + 2))
                counts[ast] -= max(0, i - 1)

        part_1 = max(counts.items(), key=lambda i: i[1])
        point = part_1[0]
        print(point)
        centered = collections.defaultdict(list)
        px, py = point
        for ast in asteroids:
            if ast == point:
                continue
            x, y = ast
            tx = py - y
            ty = x - px
            r = math.sqrt(tx * tx + ty * ty)
            angle = math.atan2(ty, tx)
            if angle < 0:
                angle = angle + math.pi * 2
            centered[angle].append((r, ast))

        for key in centered.keys():
            centered[key].sort(reverse=True)

        clock = sorted(centered.keys())
        kill_list = []
        while True:
            changed = False
            for pos in clock:
                if len(centered[pos]) > 0:
                    kill_list.append((pos, centered[pos].pop()))
                    changed = True
            if not changed:
                break
        print(kill_list[199])


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
