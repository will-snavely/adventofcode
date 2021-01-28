import collections
import itertools

test_inputs = [
    "inputs/day2"
]


def part1(boxes):
    twos = 0
    threes = 0
    for box in boxes:
        counts = collections.Counter(box)
        count_of_counts = collections.Counter(counts.values())
        if count_of_counts[2] > 0:
            twos += 1
        if count_of_counts[3] > 0:
            threes += 1
    return twos * threes


def part2(boxes):
    for b1, b2 in itertools.combinations(boxes, 2):
        same = [c1 for c1, c2 in zip(b1, b2) if c1 == c2]
        if len(same) == len(b1) - 1:
            return "".join(same)


def process(path):
    print("Input:", path)
    with open(path) as f:
        lines = []
        for line in f:
            lines.append(line.strip())
        print("\tPart 1:", part1(lines))
        print("\tPart 2:", part2(lines))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
