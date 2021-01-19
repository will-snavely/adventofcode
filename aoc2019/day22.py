import itertools

test_inputs = [
    "inputs/day22"
]


# Explicit implementation, simulating the
# full deck and table in memory
class SpaceCards1:
    def __init__(self, n):
        self.n = n
        self.cards = list(range(n))
        self.table = [0] * n

    def deal(self):
        for i in range(self.n):
            self.table[i] = self.cards[self.n - i - 1]
        temp = self.cards
        self.cards = self.table
        self.table = temp

    def cut(self, k):
        for i in range(self.n):
            self.table[i] = self.cards[(i + k) % self.n]
        temp = self.cards
        self.cards = self.table
        self.table = temp

    def increment(self, k):
        i = 0
        for j in range(self.n):
            self.table[i] = self.cards[j]
            i = (i + k) % self.n
        temp = self.cards
        self.cards = self.table
        self.table = temp

    def materialize(self):
        return self.cards

    def __repr__(self):
        return str(self.cards)

    def __getitem__(self, item):
        return self.cards[item]


# In this implementation, we just keep track of two
# values: an increment and an offset. The offset represents
# the first card of the deck. The increment represents
# how to get to the next card.
class SpaceCards2:
    def __init__(self, n):
        self.offset = 0
        self.inc = 1
        self.n = n

    def deal(self):
        self.offset = (self.offset + self.inc * (self.n - 1)) % self.n
        self.inc *= -1

    def cut(self, k):
        self.offset = (self.offset + self.inc * k) % self.n

    # Assume n is prime, here. We multiply our increment by the
    # modular inverse of k
    def increment(self, k):
        self.inc = (self.inc * pow(k, self.n - 2, self.n)) % self.n

    def materialize(self):
        for i in range(self.n):
            yield (self.offset + self.inc * i) % self.n


def shuffle(cards, steps):
    for step in steps:
        if not step:
            continue
        parts = step.split()
        if parts[0] == "deal":
            if parts[1] == "with":
                cards.increment(int(parts[-1]))
            elif parts[1] == "into":
                cards.deal()
        elif parts[0] == "cut":
            cards.cut(int(parts[-1]))


def process(path):
    with open(path) as f:
        steps = [line.strip() for line in f.readlines()]
        part1_cards = SpaceCards2(10007)
        shuffle(part1_cards, steps)
        index = 0
        for card in part1_cards.materialize():
            if card == 2019:
                print(index)
                break
            index += 1

        # For part 2, we need to do some tricky math.
        # We first perform one shuffle of the deck, and note the
        # resulting offset and increment. Call these O(1) and I(1),
        # respectively. We then are able to compute the outcome of an
        # arbitrary number of shuffles, with some simple formulas.
        #
        # The increment after K shuffles is simply:
        #  I(K) = pow(I(1), K, m)
        # Where m is the modulus.
        #
        #  O(K) = O(1) * (sum(pow(I(1), J, m) for J in range(0,K))
        # In other words, compute the sum of the geometric series
        # with base I(1), mod m. We can use the geometric series
        # formula for this, but we multiply by an inverse instead
        # of dividing.
        m = 119315717514047
        rep = 101741582076661
        part2_cards = SpaceCards2(m)
        shuffle(part2_cards, steps)
        offset = part2_cards.offset
        inc = part2_cards.inc

        # We assume here that (1 - inc) % m is prime, which in this case
        # it happens to be.
        inv = pow(1 - inc, m - 2, m)
        offset_prime = (offset * (1 - pow(inc, rep, m)) * inv) % m
        inc_prime = pow(inc, rep, m)
        part2_cards.offset = offset_prime
        part2_cards.inc = inc_prime

        count = 0
        for card in part2_cards.materialize():
            if count == 2020:
                print(card)
                return
            count += 1


def search():
    for combo in itertools.product([0, 1], repeat=8):
        print(combo)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
