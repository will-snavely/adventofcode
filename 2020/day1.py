import functools
import itertools


def part1(xs):
    diff = set([2020 - x for x in xs])
    result = list(set(xs).intersection(diff))
    for x in result:
        yield x, 2020 - x, x * (2020 - x)


def part2(xs):
    for elem in itertools.combinations(xs, 3):
        if sum(elem) == 2020:
            return elem, functools.reduce(lambda x, y: x * y, elem)


if __name__ == "__main__":
    with open("inputs/day1") as f:
        numbers = [int(line) for line in f.readlines()]
        for result in part1(numbers):
            print(result)
        for result in part2(numbers):
            print(result)
