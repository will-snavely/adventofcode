import collections

N = 0
E = 1
S = 2
W = 3

deltas = {
    N: (-1, 0),
    E: (0, 1),
    S: (1, 0),
    W: (0, -1)
}

direction = {
    "^": N,
    ">": E,
    "v": S,
    "<": W
}

reverse = {
    N: S,
    E: W,
    W: E,
    S: N
}

intersection_turn = [-1, 0, 1]

normal_turn = {
    "/": {W: S, S: W, N: E, E: N},
    "\\": {W: N, N: W, S: E, E: S},
}


class Cart:
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        self.turns = 0
        self.crashed = False

    def update_direction(self, track):
        if track == "+":
            self.dir = (self.dir + intersection_turn[self.turns % 3]) % 4
            self.turns += 1
        elif track in set("/\\"):
            self.dir = normal_turn[track][self.dir]

    def turn_at_intersection(self):
        self.dir = (self.dir + intersection_turn[self.turns % 3]) % 4
        self.turns += 1

    def move(self):
        d = deltas[self.dir]
        self.pos = (
            self.pos[0] + d[0],
            self.pos[1] + d[1]
        )


def tick(tracks, carts):
    cart_positions = {c.pos: c for c in carts if not c.crashed}
    for cart in sorted(carts, key=lambda c: c.pos):
        if cart.crashed:
            continue

        cart.update_direction(tracks[cart.pos])

        del cart_positions[cart.pos]
        cart.move()
        if cart.pos in cart_positions:
            hit = cart_positions[cart.pos]
            cart.crashed = True
            hit.crashed = True
            del cart_positions[cart.pos]
        else:
            cart_positions[cart.pos] = cart


def simulate(tracks, carts):
    while True:
        tick(tracks, carts)
        crashes = set(cart.pos for cart in carts if cart.crashed)
        for crash in crashes:
            print("Crash: {},{}".format(crash[1], crash[0]))
        carts = [cart for cart in carts if not cart.crashed]
        if len(carts) == 1:
            p = carts[0].pos
            print("Survivor: {},{}".format(p[1], p[0]))
            break


def main():
    tracks = collections.defaultdict(str)
    carts = list()
    for row, line in enumerate(open("inputs/day13")):
        for col, char in enumerate(line):
            if char in set("/-\\+|"):
                tracks[(row, col)] = char
            elif char in set("<>^v"):
                carts.append(Cart((row, col), direction[char]))
                tracks[(row, col)] = "-" if char in "<>" else "|"
    simulate(tracks, carts)


if __name__ == "__main__":
    main()
