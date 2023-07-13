import itertools

class Point:
    def __init__(self, x, y):
        self.pos = (x,y)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos

    def __add__(self, other):
        return Point(self.pos[0] + other.pos[0], self.pos[1] + other.pos[1])

    def __sub__(self, other):
        return Point(self.pos[0] - other.pos[0], self.pos[1] - other.pos[1])

    def __neg__(self):
        return Point(-self.pos[0], -self.pos[1])

    def __repr__(self):
        return "Point{}".format(self.pos)

def move_rope(steps, length):
    motion = { "R": Point(1,0), "L": Point(-1,0), "U": Point(0,-1), "D": Point(0,1) }
    rope = [Point(0,0) for _ in range(length)]
    tail_positions = set([Point(0,0)])

    for d, amt in steps:
        for _ in range(amt):
            rope[0] += motion[d]
            for i in range(length - 1):
                head = rope[i]
                tail = rope[i+1]
                diff = head - tail
                dx = 0 if diff.pos[0] == 0 else diff.pos[0] // abs(diff.pos[0])
                dy = 0 if diff.pos[1] == 0 else diff.pos[1] // abs(diff.pos[1])

                tail_move = Point(0,0)
                if abs(diff.pos[0]) == 2 or abs(diff.pos[1]) == 2:
                    tail_move = Point(dx, dy)
                rope[i+1] += tail_move
            tail_positions.add(rope[-1])
    return tail_positions

if __name__ == "__main__":
    with open("inputs/day09") as f:
        lines = [line.strip() for line in f]
        steps = []
        for line in lines:
            parts = line.split()
            steps.append((parts[0].strip(), int(parts[1].strip())))

        print(len(move_rope(steps, 2)))
        print(len(move_rope(steps, 10)))
