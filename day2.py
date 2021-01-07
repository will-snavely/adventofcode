import re


def is_valid_part1(policy, password):
    min, max, c = policy
    count = len([x for x in password if x == c])
    return min <= count <= max


def is_valid_part2(policy, password):
    i1, i2, c = policy
    return (password[i1 - 1] == c) != (password[i2 - 1] == c)


def parse_policy(text):
    result = re.match("(\d+)-(\d+)\s*(.*)", text)
    if result:
        return (
            int(result.group(1)),
            int(result.group(2)),
            result.group(3)
        )
    return None


if __name__ == "__main__":
    with open("inputs/day2") as f:
        count_part1 = 0
        count_part2 = 0
        for line in f:
            parts = line.split(":")
            policy = parse_policy(parts[0].strip())
            pwd = parts[1].strip()
            if is_valid_part1(policy, pwd):
                count_part1 += 1
            if is_valid_part2(policy, pwd):
                count_part2 += 1

        print(count_part1, count_part2)
