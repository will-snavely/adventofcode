import collections
import inspect


def parse(path):
    before = None
    instruction = None
    samples = []
    program = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Before:"):
                parts = line.split(":")
                before = eval(parts[1])
            elif line.startswith("After:"):
                parts = line.split(":")
                samples.append((before, eval(parts[1]), instruction))
                before = None
            else:
                instruction = tuple(map(int, line.split()))
                if not before:
                    program.append(instruction)
    return samples, program


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


def part1(samples):
    ops = {
        name: f
        for name, f in inspect.getmembers(Ops, predicate=inspect.isfunction)
    }
    candidates = collections.defaultdict(lambda: set(ops.keys()))
    part1_counter = 0
    for sample in samples:
        before, after, inst = sample
        local_candidates = set()
        for name, func in ops.items():
            try:
                regs = list(before)
                func(inst, regs)
                if regs == after:
                    local_candidates.add(name)
            except:
                continue

        if len(local_candidates) >= 3:
            part1_counter += 1
        candidates[inst[0]] &= local_candidates

    return part1_counter, candidates


def part2(candidates):
    determined = set()
    mapping = {}
    done = False
    while not done:
        done = True
        for op, cands in candidates.items():
            diff = cands - determined
            if len(diff) == 1:
                done = False
                singleton = list(diff)[0]
                determined.add(singleton)
                mapping[op] = singleton
    return mapping


def emulate(program, mapping):
    ops = {
        name: f
        for name, f in inspect.getmembers(Ops, predicate=inspect.isfunction)
    }
    registers = [0, 0, 0, 0]
    for inst in program:
        ops[mapping[inst[0]]](inst, registers)
    return registers


def main():
    tests = [
        "inputs/day16"
    ]
    for path in tests:
        print(path)
        samples, program = parse(path)
        counter, candidates = part1(samples)
        print("\tPart1:", counter)
        mapping = part2(candidates)
        registers = emulate(program, mapping)
        print("\tPart2:", registers[0])


if __name__ == "__main__":
    main()
