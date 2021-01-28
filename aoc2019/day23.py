import collections

test_inputs = [
    "inputs/day23"
]

from aoc2019.intcode import IntCodeProcess, IntCodeQueueIO


class NetworkIO(IntCodeQueueIO):
    def __init__(self):
        self.failed_reads = 0
        super().__init__()

    def read(self):
        if self.input:
            self.failed_reads = 0
            return self.input.popleft()
        else:
            self.failed_reads += 1
            return -1

    def fork(self):
        forked = NetworkIO()
        forked.input = self.input.copy()
        forked.output = self.output.copy()
        return forked


def part1(path):
    nic = IntCodeProcess.compile(path, io=NetworkIO)
    nodes = []
    outputs = []
    for n in range(50):
        node = nic.fork()
        node.send(n)
        outputs.append(collections.deque())
        nodes.append(node)

    while True:
        for idx, node in enumerate(nodes):
            node.simulate(budget=10)
            outputs[idx].extend(node.flush())
            while len(outputs[idx]) >= 3:
                addr = outputs[idx].popleft()
                x = outputs[idx].popleft()
                y = outputs[idx].popleft()
                if addr == 255:
                    return x, y
                nodes[addr].send(x)
                nodes[addr].send(y)


def part2(path):
    nic = IntCodeProcess.compile(path, io=NetworkIO)
    nodes = []
    outputs = []
    for n in range(50):
        node = nic.fork()
        node.send(n)
        outputs.append(collections.deque())
        nodes.append(node)

    nat_value = None
    last_nat_y = None

    while True:
        for idx, node in enumerate(nodes):
            node.simulate(budget=10)
            outputs[idx].extend(node.flush())
            while len(outputs[idx]) >= 3:
                addr = outputs[idx].popleft()
                x = outputs[idx].popleft()
                y = outputs[idx].popleft()
                if addr == 255:
                    nat_value = (x, y)
                else:
                    nodes[addr].send(x)
                    nodes[addr].send(y)

            if idx == len(nodes) - 1:
                idle = True
                for inner_node in nodes:
                    if inner_node.io.failed_reads <= 1:
                        idle = False
                        break
                if idle and nat_value is not None:
                    print(nat_value[1])
                    nodes[0].send(nat_value[0])
                    nodes[0].send(nat_value[1])
                    if last_nat_y == nat_value[1]:
                        return last_nat_y
                    last_nat_y = nat_value[1]
                    nat_value = None


def process(path):
    print(part1(path))
    print(part2(path))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
