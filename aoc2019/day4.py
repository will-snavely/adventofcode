test_inputs = [
    "inputs/day4"
]


def test(value):
    digits = [int(d) for d in str(value)]
    repeat = False
    decreasing = False
    for idx in range(1, len(digits)):
        if digits[idx] == digits[idx - 1]:
            repeat = True
        if digits[idx] < digits[idx - 1]:
            decreasing = True
    return repeat and not decreasing


def test2(value):
    digits = [int(d) for d in str(value)]
    double = False
    decreasing = False
    cur_run = 1
    for idx in range(1, len(digits)):
        if digits[idx] == digits[idx - 1]:
            cur_run += 1
        else:
            if cur_run == 2:
                double = True
            cur_run = 1
        if digits[idx] < digits[idx - 1]:
            decreasing = True
    if cur_run == 2:
        double = True
    return double and not decreasing


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            parts = [int(p) for p in line.strip().split("-")]
            print(len([d for d in range(parts[0], parts[1] + 1) if test(d)]))
            print(len([d for d in range(parts[0], parts[1] + 1) if test2(d)]))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
