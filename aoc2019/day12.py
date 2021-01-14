import collections
import itertools
import math

test_inputs = [
    "inputs/day12"
]


def lcm(*args):
    if args:
        result = args[0]
        for arg in args[1:]:
            result = lcm2(result, arg)
        return result
    return None


def lcm2(a, b):
    return abs(a * b) // math.gcd(a, b)


class Moon:
    def __init__(self, pos):
        self.p = list(pos)
        self.v = [0, 0, 0]

    def __repr__(self):
        return "{}, {}".format(self.p, self.v)

    def pe(self):
        return sum([abs(c) for c in self.p])

    def ke(self):
        return sum([abs(c) for c in self.v])


def step(moons):
    for m1, m2 in itertools.combinations(moons, 2):
        for idx, (p1, p2) in enumerate(zip(m1.p, m2.p)):
            if p1 < p2:
                m1.v[idx] += 1
                m2.v[idx] -= 1
            elif p2 < p1:
                m1.v[idx] -= 1
                m2.v[idx] += 1
    for m in moons:
        for idx in range(3):
            m.p[idx] += m.v[idx]


def parse_moon_position(line):
    line = line.replace("<", "").replace(">", "")
    parts = line.split(",")
    return tuple([int(part.split("=")[1]) for part in parts])


def process(path):
    print("Input:", path)
    seen = set()
    with open(path) as f:
        moons = [Moon(parse_moon_position(line)) for line in f.readlines()]
        cycle_len = {}
        history = collections.defaultdict(set)
        for i in range(3):
            history[i].add(tuple([(m.p[i], m.v[i]) for m in moons]))

        n = 0
        while len(cycle_len) < 3:
            n += 1
            step(moons)
            # energy = sum([m.pe() * m.ke() for m in moons])

            for i in range(3):
                if i in cycle_len:
                    continue
                code = tuple([(m.p[i], m.v[i]) for m in moons])
                if code in history[i]:
                    cycle_len[i] = n
                else:
                    history[i].add(tuple([(m.p[i], m.v[i]) for m in moons]))
        print(lcm(*list(cycle_len.values())))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
