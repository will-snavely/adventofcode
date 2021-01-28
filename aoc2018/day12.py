import collections


def step(state, rules):
    next_state = collections.defaultdict(bool)
    values = list(filter(lambda k: state[k], list(state.keys())))
    left = min(values)
    right = max(values)
    for x in range(left - 2, right + 3):
        next_state[x] = rules[tuple(state[i] for i in range(x - 2, x + 3))]
    return next_state


def render(state):
    values = state.keys()
    left = min(values)
    right = max(values)
    print("".join("#" if state[x] else "." for x in range(left, right + 1)))


def part1(initial_state, rules):
    state = initial_state
    for _ in range(20):
        state = step(state, rules)
    return sum(x for x in state if state[x])


def part2(initial_state, rules):
    state = initial_state
    repeat_point = 92
    repeat_val = 80
    target = 50000000000

    for x in range(repeat_point):
        state = step(state, rules)
    val = sum(x for x in state if state[x])
    return val + (target - repeat_point) * repeat_val


def main():
    initial_state = collections.defaultdict(bool)
    rules = collections.defaultdict(bool)
    for line in open("inputs/day12"):
        line = line.strip()
        if not line:
            continue
        elif line.startswith("initial state"):
            parts = line.split(":")
            for idx, c in enumerate(parts[1].strip()):
                if c == "#":
                    initial_state[idx] = True
        else:
            parts = line.split("=>")
            lhs = tuple(c == "#" for c in parts[0].strip())
            rhs = parts[1].strip() == "#"
            rules[lhs] = rhs
    print(part1(initial_state, rules))
    print(part2(initial_state, rules))


if __name__ == "__main__":
    main()
