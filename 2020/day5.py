def decode(s, bitmap):
    powers = [2 ** i for i in range(len(s))]
    bits = [bitmap[c] for c in s]
    return sum([x * y for (x, y) in zip(bits, reversed(powers))])


def get_seat_number(ticket):
    row = ticket[:7]
    seat = ticket[7:]
    return 8 * decode(row, {"F": 0, "B": 1}) + decode(seat, {"L": 0, "R": 1})


if __name__ == "__main__":
    with open("inputs/day5") as f:
        seats = set([get_seat_number(line.strip()) for line in f])
        print(max(seats))
        print(set(range(min(seats), max(seats))) - seats)
