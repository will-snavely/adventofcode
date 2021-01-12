import itertools

from aoc2019.intcode2 import IntCodeProcess

test_inputs = [
    "inputs/day7"
]


def part1(program):
    values = []
    for config in itertools.permutations(range(0, 5)):
        arg = 0
        for var in config:
            proc = IntCodeProcess(program)
            proc.send(var)
            proc.send(arg)
            proc.run()
            arg = proc.flush()[0]
        values.append((arg, config))
    return max(values)


def part2(program):
    values = []
    for config in itertools.permutations(range(5, 10)):
        procs = [IntCodeProcess(program, [var]) for var in config]
        procs[0].send(0)
        done = False
        while not done:
            for pid, proc in enumerate(procs):
                proc.run()
                if proc.done() and pid == len(procs) - 1:
                    values.extend(proc.flush())
                    done = True
                else:
                    for out in proc.flush():
                        procs[(pid + 1) % len(procs)].send(out)

    return max(values)


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            program = [int(x) for x in line.split(",")]
            print(part1(program))
            print(part2(program ))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
