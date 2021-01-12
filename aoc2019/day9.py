test_inputs = [
    "inputs/day9"
]

from aoc2019.intcode2 import IntCodeProcess


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            program = [int(c) for c in line.split(",")]
            proc = IntCodeProcess(program)
            proc.send(2)
            proc.run()
            for o in proc.output:
                print(o)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
