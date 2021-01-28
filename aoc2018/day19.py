import inspect

A = 1
B = 2
C = 3


class Ops:
    @staticmethod
    def addr(inst, mem):
        mem[inst[C]] = mem[inst[A]] + mem[inst[B]]

    @staticmethod
    def addi(inst, mem):
        mem[inst[C]] = mem[inst[A]] + inst[B]

    @staticmethod
    def mulr(inst, mem):
        mem[inst[C]] = mem[inst[A]] * mem[inst[B]]

    @staticmethod
    def muli(inst, mem):
        mem[inst[C]] = mem[inst[A]] * inst[B]

    @staticmethod
    def banr(inst, mem):
        mem[inst[C]] = mem[inst[A]] & mem[inst[B]]

    @staticmethod
    def bani(inst, mem):
        mem[inst[C]] = mem[inst[A]] & inst[B]

    @staticmethod
    def borr(inst, mem):
        mem[inst[C]] = mem[inst[A]] | mem[inst[B]]

    @staticmethod
    def bori(inst, mem):
        mem[inst[C]] = mem[inst[A]] | inst[B]

    @staticmethod
    def setr(inst, mem):
        mem[inst[C]] = mem[inst[A]]

    @staticmethod
    def seti(inst, mem):
        mem[inst[C]] = inst[A]

    @staticmethod
    def gtir(inst, mem):
        mem[inst[C]] = 1 if inst[A] > mem[inst[B]] else 0

    @staticmethod
    def gtri(inst, mem):
        mem[inst[C]] = 1 if mem[inst[A]] > inst[B] else 0

    @staticmethod
    def gtrr(inst, mem):
        mem[inst[C]] = 1 if mem[inst[A]] > mem[inst[B]] else 0

    @staticmethod
    def eqir(inst, mem):
        mem[inst[C]] = 1 if inst[A] == mem[inst[B]] else 0

    @staticmethod
    def eqri(inst, mem):
        mem[inst[C]] = 1 if mem[inst[A]] == inst[B] else 0

    @staticmethod
    def eqrr(inst, mem):
        mem[inst[C]] = 1 if mem[inst[A]] == mem[inst[B]] else 0


def emulate(program, ip_register, registers):
    ops = {
        name: f
        for name, f in inspect.getmembers(Ops, predicate=inspect.isfunction)
    }
    ip = 0
    while 0 <= ip < len(program):
        instruction = program[ip]
        op_name = instruction[0]
        registers[ip_register] = ip
        ops[op_name](instruction, registers)
        ip = registers[ip_register] + 1
    return registers


def main():
    tests = [
        "inputs/day19"
    ]
    for path in tests:
        with open(path) as f:
            program = []
            for line in f:
                if line.startswith("#ip"):
                    ip_binding = int(line.split()[1])
                else:
                    parts = line.split()
                    program.append([parts[0]] + [int(x) for x in parts[1:4]])
        registers = emulate(program, ip_binding, [0, 0, 0, 0, 0, 0])
        print(registers)

        # This is too slow to run...
        # But reverse engineering the program reveals that
        # it is summing the divisors of 10551367 (including 1 and 10551367)
        # very inefficiently. The result is therefore:
        print(1 + 2801 + 3767 + 10551367)
        # registers = emulate(program, ip_binding, [1, 0, 0, 0, 0, 0])
        # print(registers)


if __name__ == "__main__":
    main()
