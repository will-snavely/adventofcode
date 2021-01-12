import itertools

test_inputs = [
    "inputs/day14_sample_2",
    "inputs/day14",
]

import pyparsing as pp

MemRef = pp.Literal("mem")
MaskRef = pp.Literal("mask")
MaskValue = pp.Word("X" + pp.nums)
Integer = pp.Word(pp.nums)
MaskAssign = MaskRef + "=" + MaskValue.setResultsName("value")
MemAssign = MemRef + "[" + Integer.setResultsName("index") + "]" + "=" + Integer.setResultsName("value")
Statement = MaskAssign.setResultsName("mask") | MemAssign.setResultsName("mem")


def int_to_bit_array(num, pad=None):
    result = []
    while num > 0:
        bit = num % 2
        result.append(bit)
        num = num // 2

    if pad and pad > len(result):
        pad_len = pad - len(result)
        result = result + [0] * pad_len
    return result


def bit_array_to_int(bit_array):
    powers = [2 ** i for i in range(len(bit_array))]
    return sum([p * b for p, b in zip(powers, bit_array)])


class InterpreterV1:
    def __init__(self):
        self.memory = {}
        self.mask = None

    def interpret_mask_assign(self, value):
        self.mask = list(reversed(value))

    def interpret_mem_assign(self, index, value):
        bit_array = int_to_bit_array(value, pad=len(self.mask))
        bit_index = 0
        for bit in self.mask:
            if bit != "X":
                bit_array[bit_index] = int(bit)
            bit_index += 1
        self.memory[index] = bit_array_to_int(bit_array)

    def interpret(self, line):
        parsed = Statement.parseString(line)
        if "mask" in parsed:
            value = parsed["value"]
            self.interpret_mask_assign(value)
        elif "mem" in parsed:
            index = int(parsed["index"])
            value = int(parsed["value"])
            self.interpret_mem_assign(index, value)


class InterpreterV2:
    def __init__(self):
        self.memory = {}
        self.mask = None

    def interpret_mask_assign(self, value):
        self.mask = list(reversed(value))

    def interpret_mem_assign(self, index, value):
        bit_array = int_to_bit_array(index, pad=len(self.mask))
        bit_index = 0
        for bit in self.mask:
            if bit == "1":
                bit_array[bit_index] = 1
            elif bit == "X":
                bit_array[bit_index] = None
            bit_index += 1

        none_count = len([b for b in bit_array if b is None])
        for bit_assignment in itertools.product([0, 1], repeat=none_count):
            cur = bit_array.copy()
            assignment_index = 0
            for index in range(len(cur)):
                if cur[index] is None:
                    cur[index] = bit_assignment[assignment_index]
                    assignment_index += 1
            self.memory[bit_array_to_int(cur)] = value

    def interpret(self, line):
        parsed = Statement.parseString(line)
        if "mask" in parsed:
            value = parsed["value"]
            self.interpret_mask_assign(value)
        elif "mem" in parsed:
            index = int(parsed["index"])
            value = int(parsed["value"])
            self.interpret_mem_assign(index, value)


def process(path):
    print("Input:", path)
    interp1 = InterpreterV1()
    interp2 = InterpreterV2()
    with open(path) as f:
        for line in f:
            interp1.interpret(line)
            interp2.interpret(line)
        print("\tPart 1 Sum:", sum(interp1.memory.values()))
        print("\tPart 1 Sum:", sum(interp2.memory.values()))

def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
