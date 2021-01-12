def load_program(path):
    with open(path) as f:
        for line in f:
            parts = line.split()
            op = parts[0]
            arg = int(parts[1])
            yield op, arg


def interpret(program):
    pc = 0
    accumulator = 0
    visited = set()

    while True:
        if pc == len(program):
            return True, accumulator
        op, arg = program[pc]
        if pc in visited:
            return False, accumulator

        visited.add(pc)
        if op == "acc":
            accumulator += arg
            pc += 1
        elif op == "jmp":
            pc += arg
        elif op == "nop":
            pc += 1


def main():
    program = list(load_program("inputs/day8"))
    print(interpret(program))
    for idx in range(0, len(program)):
        op, arg = program[idx]
        if op == "jmp":
            program[idx] = ("nop", arg)
            terminated, acc = interpret(program)
            if terminated:
                print(acc)
            program[idx] = (op, arg)
        if op == "nop":
            program[idx] = ("jmp", arg)
            terminated, acc = interpret(program)
            if terminated:
                print(acc)
            program[idx] = (op, arg)


if __name__ == "__main__":
    main()
