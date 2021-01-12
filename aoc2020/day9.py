import itertools

test_inputs = [
    ("inputs/day9_sample", 5),
    ("inputs/day9", 25)
]


def possible_sums(summands):
    return set([x + y for x, y in itertools.combinations(summands, 2) if x != y])


def validate(cipher, preamble_len):
    idx = preamble_len
    while idx < len(cipher):
        summands = cipher[idx - preamble_len:idx]
        value = cipher[idx]
        if value not in possible_sums(summands):
            return False, value, idx
        idx += 1
    return True, None, None


def find_contiguous_sum(start, end, target, xs):
    for l, r in itertools.combinations(range(start, end), 2):
        if sum(xs[l:r]) == target:
            return min(xs[l:r]) + max(xs[l:r])


def process(path, preamble_len):
    with open(path) as f:
        cipher = [int(line) for line in f]
        valid, mismatch, idx = validate(cipher, preamble_len)
        if not valid:
            print("Bad ciphertext:", mismatch)
            print((find_contiguous_sum(0, idx, mismatch, cipher)))


def main():
    for path, preamble_len in test_inputs:
        process(path, preamble_len)


if __name__ == "__main__":
    main()
