import collections

test_inputs = [
    "inputs/day10_sample_1",
    "inputs/day10_sample_2",
    "inputs/day10"
]


def count_valid(ratings):
    idx = len(ratings) - 1
    count_starting_from = collections.defaultdict(int)
    count_starting_from[idx] = 1
    idx -= 1

    while idx >= 0:
        for next in range(idx + 1, len(ratings)):
            if ratings[next] - ratings[idx] <= 3:
                count_starting_from[idx] += count_starting_from[next]
            else:
                break
        idx -= 1
    return count_starting_from


def process(path):
    with open(path) as f:
        joltage_ratings = sorted([int(line) for line in f])
        prev = 0
        diff_map = collections.defaultdict(int)
        for rating in joltage_ratings:
            diff = rating - prev
            prev = rating
            diff_map[diff] += 1
        print(path)
        print("\tPart 1:", diff_map[1] * (diff_map[3] + 1))

        ratings_with_zero = [0] + joltage_ratings
        count_starting_from = count_valid(ratings_with_zero)
        print("\tPart 2:", count_starting_from[0])


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
