import collections

test_inputs = [
    "inputs/day15",
]


class NumberRecord:
    def __init__(self):
        self.most_recent = None
        self.second_most_recent = None

    def update(self, value):
        self.second_most_recent = self.most_recent
        self.most_recent = value


class NumberGame:
    def __init__(self, iv):
        self.turn = 1
        self.record = collections.defaultdict(NumberRecord)
        self.last_spoken = None
        for num in iv:
            self.starting_turn(num)

    def starting_turn(self, number):
        self.record[number].update(self.turn)
        self.last_spoken = number
        self.turn += 1

    def normal_turn(self, starting_number=None):
        history = self.record[self.last_spoken]
        if history.second_most_recent is None:
            next_number = 0
        else:
            next_number = history.most_recent - history.second_most_recent

        turn_tmp = self.turn
        self.record[next_number].update(self.turn)
        self.last_spoken = next_number
        self.turn += 1
        return turn_tmp, next_number


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            seq = [int(x) for x in line.strip().split(",")]
            print(seq)
            game = NumberGame(seq)

            while True:
                turn, val = game.normal_turn()
                if turn == 30000000:
                    break
            print(turn, val)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
