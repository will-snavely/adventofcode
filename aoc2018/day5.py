import string

test_inputs = [
    "inputs/day5"
]


def react(polymer, banned=None):
    stack = []
    for p in polymer:
        if banned and p in banned:
            continue
        if stack:
            top = stack[-1]
            if top.upper() == p.upper() and top != p:
                stack.pop()
            else:
                stack.append(p)
        else:
            stack.append(p)
    return stack


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            polymer = line.strip()
            print(len(react(polymer)))
            part2 = min(
                len(react(polymer, banned={c, c.upper()}))
                for c in string.ascii_lowercase
            )
            print(part2)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
