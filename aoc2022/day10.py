import itertools

class CRT:
    def __init__(self):
        self.cycle = 0
        self.sprite = 1
        self.signal = 0
        self.screen = ["." for _ in range(240)]

    def step(self, dx=0):
        middle = (self.cycle) % 40
        if abs(self.sprite - middle) <= 1:
            self.screen[self.cycle] = "#"

        self.cycle += 1
        if (self.cycle - 20) % 40 == 0:
            self.signal += self.cycle * self.sprite
        self.sprite += dx

    def __str__(self):
        s = ""
        for row in range(6):
            s += "".join(self.screen[row*40:(row+1)*40]) + "\n"
        return s


if __name__ == "__main__":
    with open("inputs/day10") as f:
        lines = [line.strip() for line in f]
        cmds = []
        for line in lines:
            parts = line.split()
            if parts[0] == "noop":
                cmds.append(("noop",))
            elif parts[0] == "addx":
                cmds.append(("addx", int(parts[1])))
        
        crt = CRT()
        for cmd in cmds:
            if cmd[0] == "noop":
                crt.step()
            elif cmd[0] == "addx":
                crt.step()
                crt.step(cmd[1])

        print(crt.signal)
        print(str(crt))
