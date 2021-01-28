import collections
import re

test_inputs = [
    "inputs/day3"
]

# 1 @ 1,3: 4x4
claim_pattern = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def parse_claim(line):
    match = claim_pattern.match(line)
    if match:
        return tuple(int(match.group(x)) for x in range(1, 6))
    return None


def solve(claims):
    counter = collections.defaultdict(int)
    for claim in claims:
        _, x, y, w, h = claim
        for i in range(x, x + w):
            for j in range(y, y + h):
                counter[(i, j)] += 1

    non_overlapping = []
    for claim in claims:
        _, x, y, w, h = claim
        overlaps = False
        for i in range(x, x + w):
            for j in range(y, y + h):
                if counter[(i, j)] > 1:
                    overlaps = True
                    break
        if not overlaps:
            non_overlapping.append(claim)

    return len([k for k in counter if counter[k] > 1]), non_overlapping


def process(path):
    print("Input:", path)
    with open(path) as f:
        claims = [parse_claim(line) for line in f]
        result = solve(claims)
        print("\tPart 1:", result[0])
        print("\tPart 2:", result[1])


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
