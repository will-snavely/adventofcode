test_inputs = [
    "inputs/day1"
]


def fuel1(mass):
    return (mass // 3) - 2


def fuel2(mass):
    result = 0
    while True:
        mass = (mass // 3) - 2
        if mass > 0:
            result += mass
        else:
            break
    return result


def process(path):
    print("Input:", path)
    with open(path) as f:
        masses = [int(line) for line in f.readlines()]
        print("\tPart 1:", sum([fuel1(m) for m in masses]))
        print("\tPart 2:", sum([fuel2(m) for m in masses]))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
