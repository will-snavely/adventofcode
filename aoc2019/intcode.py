import collections


def parse_instruction(instruction):
    s = str(instruction)
    opcode = int(s[-2:])
    flags = [int(f) for f in reversed(s[:-2])]
    return opcode, flags


class IntCodeIO:
    def __init__(self):
        pass

    def read(self):
        raise NotImplemented

    def send(self, value):
        raise NotImplemented

    def write(self, value):
        raise NotImplemented

    def flush(self):
        raise NotImplemented

    def fork(self):
        raise NotImplemented


class IntCodeQueueIO(IntCodeIO):
    def __init__(self):
        super().__init__()
        self.input = collections.deque()
        self.output = collections.deque()

    def read(self):
        if self.input:
            return self.input.popleft()
        return None

    def send(self, value):
        self.input.append(value)

    def write(self, value):
        self.output.append(value)

    def flush(self):
        result = []
        while self.output:
            result.append(self.output.popleft())
        return result

    def fork(self):
        forked = IntCodeQueueIO()
        forked.input = self.input.copy()
        forked.output = self.output.copy()
        return forked


class IntCodeProcess:
    def __init__(self, program, args=None, io=IntCodeQueueIO):
        self.memory = collections.defaultdict(int)

        self.io = None
        if io is not None:
            self.io = io()

        if args:
            for arg in args:
                self.io.send(arg)

        self.state = "idle"
        self.pc = 0
        self.rbo = 0

        if program:
            for index, instruction in enumerate(program):
                self.memory[index] = instruction

    @classmethod
    def compile(cls, path, args=None, io=IntCodeQueueIO):
        code = []
        with open(path) as f:
            for line in f:
                stripped = line.strip().strip(",")
                code.extend([int(x) for x in stripped.split(",")])
        return cls(code, args=args, io=io)

    def done(self):
        return self.state == "done"

    def fork(self):
        forked = IntCodeProcess(None, io=None)
        forked.memory = self.memory.copy()
        forked.io = self.io.fork()
        forked.pc = self.pc
        forked.rbo = self.rbo
        forked.state = self.state
        return forked

    def send(self, *args):
        for arg in args:
            self.io.send(arg)
            # self.input.append(arg)

    def flush(self):
        return self.io.flush()

    def load(self, addr, flag=1):
        if flag == 0 or flag is None:
            return self.memory[self.memory[addr]]
        elif flag == 1:
            return self.memory[addr]
        elif flag == 2:
            return self.memory[self.memory[addr] + self.rbo]

    def load_n(self, start, n, flags=None):
        result = []
        for idx in range(n):
            flag = None
            if idx < len(flags):
                flag = flags[idx]
            result.append(self.load(start + idx, flag=flag))
        return result

    def store(self, addr, value):
        self.memory[addr] = value

    def apply_flags(self, flags, values):
        result = []
        for flag, value in zip(flags, values):
            if flag == 1:
                result.append(value)
            else:
                result.append(self.load(value))
        return result

    def run(self, budget=None):
        if self.state == "done":
            return
        self.state = "running"

        if budget is not None and budget < 1:
            return

        while True:
            opcode, flags = parse_instruction(self.load(self.pc))
            if opcode == 1:  # Add
                args = self.load_n(self.pc + 1, 2, flags)
                dest = self.load(self.pc + 3)
                if len(flags) >= 3 and flags[2] == 2:
                    dest += self.rbo
                self.store(dest, args[0] + args[1])
                self.pc += 4
            elif opcode == 2:  # Mult
                args = self.load_n(self.pc + 1, 2, flags)
                dest = self.load(self.pc + 3)
                if len(flags) >= 3 and flags[2] == 2:
                    dest += self.rbo
                self.store(dest, args[0] * args[1])
                self.pc += 4
            elif opcode == 3:  # Read
                dest = self.load(self.pc + 1)
                if len(flags) >= 1 and flags[0] == 2:
                    dest += self.rbo
                value = self.io.read()
                if value is not None:
                    # value = self.input.popleft()
                    self.store(dest, value)
                    self.pc += 2
                else:
                    self.state = "blocked"
                    return
            elif opcode == 4:  # Write
                flag = 0
                if flags:
                    flag = flags[0]
                self.io.write(self.load(self.pc + 1, flag))
                self.pc += 2
            elif opcode == 5:  # Jump If True
                args = self.load_n(self.pc + 1, 2, flags)
                if args[0] != 0:
                    self.pc = args[1]
                else:
                    self.pc += 3
            elif opcode == 6:  # Jump If False
                args = self.load_n(self.pc + 1, 2, flags)
                if args[0] == 0:
                    self.pc = args[1]
                else:
                    self.pc += 3
            elif opcode == 7:  # Less Than
                args = self.load_n(self.pc + 1, 2, flags)
                dest = self.load(self.pc + 3)
                if len(flags) >= 3 and flags[2] == 2:
                    dest += self.rbo
                if args[0] < args[1]:
                    self.store(dest, 1)
                else:
                    self.store(dest, 0)
                self.pc += 4
            elif opcode == 8:  # Equals
                args = self.load_n(self.pc + 1, 2, flags)
                dest = self.load(self.pc + 3)
                if len(flags) >= 3 and flags[2] == 2:
                    dest += self.rbo
                if args[0] == args[1]:
                    self.store(dest, 1)
                else:
                    self.store(dest, 0)
                self.pc += 4
            elif opcode == 9:  # Adjust RBO
                flag = 0
                if flags:
                    flag = flags[0]
                amount = self.load(self.pc + 1, flag)
                self.rbo += amount
                self.pc += 2
            elif opcode == 99:
                self.state = "done"
                return
            if budget is not None:
                budget = budget - 1
                if budget <= 0:
                    return
