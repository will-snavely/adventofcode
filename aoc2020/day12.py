import math

test_inputs = [
    "inputs/day12_sample",
    "inputs/day12"
]


class WaypointNavigation:
    def __init__(self):
        self.ship = [0, 0]
        self.waypoint = [10, 1]

    def rotate_counterclockwise(self, amt):
        cos = math.cos(math.radians(amt))
        sin = math.sin(math.radians(amt))
        relx = self.waypoint[0] - self.ship[0]
        rely = self.waypoint[1] - self.ship[1]
        rotx = cos * relx + -1 * sin * rely
        roty = sin * relx + cos * rely
        self.waypoint[0] = int(self.ship[0] + rotx)
        self.waypoint[1] = int(self.ship[1] + roty)

    def navigate(self, op, amount):
        if op == "N":
            self.waypoint[1] += amount
        elif op == "S":
            self.waypoint[1] -= amount
        elif op == "E":
            self.waypoint[0] += amount
        elif op == "W":
            self.waypoint[0] -= amount
        elif op == "L":
            self.rotate_counterclockwise(amount)
        elif op == "R":
            self.rotate_counterclockwise(amount * -1)
        elif op == "F":
            dx = (self.waypoint[0] - self.ship[0]) * amount
            dy = (self.waypoint[1] - self.ship[1]) * amount
            self.ship[0] += dx
            self.ship[1] += dy
            self.waypoint[0] += dx
            self.waypoint[1] += dy


class Ship:
    def __init__(self, direction):
        self.direction_map = {
            "N": 0,
            "E": 1,
            "S": 2,
            "W": 3
        }

        self.direction = self.direction_map[direction]
        self.x = 0
        self.y = 0

    def turn(self, deg):
        deg = deg % 360
        assert deg % 90 == 0
        quads = int(deg / 90)
        self.direction = (self.direction + quads) % 4

    def move(self, op, amount):
        if op == "N":
            self.y += amount
        elif op == "S":
            self.y -= amount
        elif op == "E":
            self.x += amount
        elif op == "W":
            self.x -= amount
        elif op == "L":
            self.turn(-1 * amount)
        elif op == "R":
            self.turn(amount)
        elif op == "F":
            if self.direction == 0:
                self.move("N", amount)
            elif self.direction == 1:
                self.move("E", amount)
            elif self.direction == 2:
                self.move("S", amount)
            elif self.direction == 3:
                self.move("W", amount)


def process(path):
    print("Input:", path)
    instructions = []
    with open(path) as f:
        for line in f:
            op = line[0]
            amt = int(line[1:])
            instructions.append((op, amt))

    ship = Ship("E")
    for op, amt in instructions:
        ship.move(op, amt)
    print("\tDistance 1:", abs(ship.x) + abs(ship.y))

    nav = WaypointNavigation()
    for op, amt in instructions:
        nav.navigate(op, amt)
        print(op, amt, nav.ship, nav.waypoint)
    print("\tDistance 2:", abs(nav.ship[0]) + abs(nav.ship[1]))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
