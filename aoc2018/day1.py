test_inputs = [
    "inputs/day1"
]


def part1(deltas):
    return sum(deltas)


def part2(deltas):
    cur = 0
    seen = {0}
    while True:
        for d in deltas:
            cur += d
            if cur in seen:
                return cur
            seen.add(cur)


def process(path):
    print("Input:", path)
    with open(path) as f:
        deltas = [int(line) for line in f.readlines()]
        print("\tPart 1:", part1(deltas))
        print("\tPart 2:", part2(deltas))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
