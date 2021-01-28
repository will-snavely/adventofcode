import collections
import itertools

test_inputs = [
    "inputs/day6"
]


def dist(p1, p2):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def points_at_dist(center, d):
    if d == 0:
        yield center
    else:
        x = center[0]
        y = center[1] + d
        deltas = [(1, -1), (-1, -1), (-1, 1), (1, 1)]
        for ds in deltas:
            for i in range(d):
                x += ds[0]
                y += ds[1]
                yield x, y


def closest_points(p, points):
    distance = collections.defaultdict(list)
    for q in points:
        distance[dist(p, q)].append(q)
    return distance[min(distance.keys())]


def part1(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x1, x2 = min(xs), max(xs)
    y1, y2 = min(ys), max(ys)
    area = collections.defaultdict(int)
    infinite = set()
    for p in itertools.product(range(x1, x2 + 1), range(y1, y2 + 1)):
        closest = closest_points(p, points)
        if len(closest) == 1:
            if p[0] in [x1, x2] or p[1] in [y1, y2]:
                infinite.add(closest[0])
            else:
                area[closest[0]] += 1
    return max(area[p] for p in area if p not in infinite)


def part2(points, threshold):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    mid = (sum(xs) // len(xs), sum(ys) // len(ys))
    d = 0
    region_size = 0
    while True:
        changed = False
        for p in points_at_dist(mid, d):
            total_dist = sum(dist(p, q) for q in points)
            if total_dist < threshold:
                region_size += 1
                changed = True
        if not changed:
            return region_size
        d += 1


def process(path):
    with open(path) as f:
        points = set([
            tuple(int(p) for p in line.split(","))
            for line in f
        ])
        print(part1(points))
        print(part2(points, 10000))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
