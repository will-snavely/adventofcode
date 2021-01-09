"""
Requires computing a discrete log and a modular exponent.
Inefficient, bespoke functions were written for both,
but the final solution uses faster algorithms from libraries.
Namely, we use sympy's discrete_log function, and pythons
built-in modular exponentiation (pow),
"""
test_inputs = [
    "inputs/day25_sample",
    "inputs/day25",
]

from sympy.ntheory.residue_ntheory import discrete_log


def find_loop_size(pk, iv, m):
    count = 0
    val = 1
    while True:
        if pk == val:
            return count
        val = (val * iv) % m
        count += 1


def transform(subject, loop, m):
    result = 1
    for _ in range(loop):
        result = (result * subject) % m
    return result


def solve(card_pk, door_pk):
    base = 7
    m = 20201227
    card_loop_size = discrete_log(m, card_pk, base)
    door_loop_size = discrete_log(m, door_pk, base)
    return (
        pow(door_pk, card_loop_size, m),
        pow(card_pk, door_loop_size, m)
    )


def process(path):
    print("Input:", path)
    with open(path) as f:
        pks = [int(line) for line in f]
        card_pk, door_pk = pks
        print("\tKey:", solve(card_pk, door_pk))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
