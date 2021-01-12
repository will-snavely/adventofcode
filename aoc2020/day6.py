import functools


def get_answer_groups(path):
    with open(path) as f:
        grp = []
        for line in f:
            stripped = line.strip()
            if stripped:
                grp.append(set(stripped))
            else:
                yield grp
                grp = []
    if grp:
        yield grp


if __name__ == "__main__":
    groups = get_answer_groups("inputs/day6")
    part1_count = 0
    part2_count = 0
    for group in groups:
        union = functools.reduce(lambda s, t: s.union(t), group)
        intersect = functools.reduce(lambda s, t: s.intersection(t), group)
        part1_count += len(union)
        part2_count += len(intersect)
    print(part1_count)
    print(part2_count)
