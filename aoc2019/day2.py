import itertools

from aoc2019 import intcode2

test_inputs = [
    "inputs/day2"
]


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            program = [int(x) for x in line.split(",")]
            proc = intcode2.IntCodeProcess(program)
            proc.memory[1] = 12
            proc.memory[2] = 2
            proc.run()
            print("\tPart 1:", proc.memory[0])

            target = 19690720
            for n, v in itertools.product(range(100), repeat=2):
                proc = intcode2.IntCodeProcess(program)
                proc.memory[1] = n
                proc.memory[2] = v
                proc.run()
                if proc.memory[0] == target:
                    print("\tPart 2:", n, v, 100 * n + v)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
