from aoc2019 import intcode2

test_inputs = [
    "inputs/day5"
]


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            program = [int(x) for x in line.split(",")]
            proc1 = intcode2.IntCodeProcess(program)
            proc1.send(1)
            proc1.run()
            print(proc1.flush())

            proc2 = intcode2.IntCodeProcess(program)
            proc2.send(5)
            proc2.run()
            print(proc2.flush())


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
