import collections

import pyparsing as pp

test_inputs = [
    "inputs/day22_sample",
    "inputs/day22"
]

Integer = pp.Word(pp.nums).setParseAction(pp.tokenMap(int))
Player1 = pp.Literal("Player 1:")
Player2 = pp.Literal("Player 2:")
Specification = pp.Group(Player1 + pp.ZeroOrMore(Integer)("deck"))("p1") \
                + pp.Group(Player2 + pp.ZeroOrMore(Integer)("deck"))("p2")


def round_part1(p1: collections.deque, p2: collections.deque):
    if not p1 or not p2:
        return p1, p2

    p1_top = p1.popleft()
    p2_top = p2.popleft()
    p1_next = collections.deque(p1)
    p2_next = collections.deque(p2)
    if p1_top > p2_top:
        p1_next.append(p1_top)
        p1_next.append(p2_top)
    else:
        p2_next.append(p2_top)
        p2_next.append(p1_top)
    return p1_next, p2_next


def score(deck):
    return sum([card * idx for (card, idx) in zip(deck, range(len(deck), 0, -1))])


def part1(spec):
    p1_deck = collections.deque(spec["p1"]["deck"])
    p2_deck = collections.deque(spec["p2"]["deck"])

    while True:
        p1_deck, p2_deck = round_part1(p1_deck, p2_deck)
        if not p1_deck or not p2_deck:
            break
    if p1_deck:
        print("\tPart 1 -- P1 Wins:", score(p1_deck))
    else:
        print("\tPart 1 -- P2 Wins:", score(p2_deck))


class RecursiveCombatGameState:
    def __init__(self, p1_deck, p2_deck):
        self.p1_deck = collections.deque(p1_deck)
        self.p2_deck = collections.deque(p2_deck)
        self.p1_top = None
        self.p2_top = None
        self.history = set()
        self.round = 0

    def seen_state_before(self):
        p1 = tuple(self.p1_deck)
        p2 = tuple(self.p2_deck)
        return (p1, p2) in self.history


def part2(spec):
    p1_deck = collections.deque(spec["p1"]["deck"])
    p2_deck = collections.deque(spec["p2"]["deck"])

    game_stack = list()
    cur_game = RecursiveCombatGameState(p1_deck, p2_deck)

    while True:
        forced_win = False
        if cur_game.seen_state_before():
            forced_win = True
        else:
            cur_game.round += 1
            cur_game.history.add((tuple(cur_game.p1_deck), tuple(cur_game.p2_deck)))
            cur_game.p1_top = cur_game.p1_deck.popleft()
            cur_game.p2_top = cur_game.p2_deck.popleft()
            p1_remaining = len(cur_game.p1_deck)
            p2_remaining = len(cur_game.p2_deck)

            if cur_game.p1_top > p1_remaining or cur_game.p2_top > p2_remaining:
                if cur_game.p1_top > cur_game.p2_top:
                    cur_game.p1_deck.append(cur_game.p1_top)
                    cur_game.p1_deck.append(cur_game.p2_top)
                else:
                    cur_game.p2_deck.append(cur_game.p2_top)
                    cur_game.p2_deck.append(cur_game.p1_top)
            else:
                game_stack.append(cur_game)
                cur_game = RecursiveCombatGameState(
                    list(cur_game.p1_deck)[:cur_game.p1_top],
                    list(cur_game.p2_deck)[:cur_game.p2_top])

        winner = None
        while True:
            if not cur_game.p2_deck or forced_win:
                forced_win = False
                if game_stack:
                    cur_game = game_stack.pop()
                    cur_game.p1_deck.append(cur_game.p1_top)
                    cur_game.p1_deck.append(cur_game.p2_top)
                else:
                    winner = ("P1", cur_game.p1_deck)
                    break
            elif not cur_game.p1_deck:
                if game_stack:
                    cur_game = game_stack.pop()
                    cur_game.p2_deck.append(cur_game.p2_top)
                    cur_game.p2_deck.append(cur_game.p1_top)
                else:
                    winner = ("P2", cur_game.p2_deck)
                    break
            else:
                break

        if winner is not None:
            break

    print("\tPart 2 -- {} Wins".format(winner[0]), score(winner[1]))


def process(path):
    print("Input:", path)

    with open(path) as f:
        spec = Specification.parseString(f.read())
    part1(spec)
    part2(spec)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
