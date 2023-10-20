import itertools

def compare(left, right): 
    if isinstance(left, int):
        if isinstance(right, int):
            return left - right
        if isinstance(right, list):
            return compare([left], right)
        return None
    elif isinstance(left, list):
        if isinstance(right, int):
            return compare(left, [right])
        if isinstance(right, list):
            for idx in range(len(left)):
                if idx >= len(right):
                    return 1
                cmp = compare(left[idx], right[idx])
                if cmp != 0:
                    return cmp
            if len(right) > len(left):
                return -1
            return 0
        return None
    return None


if __name__ == "__main__":
    with open("aoc2022/inputs/day13") as f:
        lines = [line.strip() for line in f]
        packets = [eval(line) for line in lines if line]
        idx = 1
        sum = 0
        for (left, right) in itertools.batched(packets, 2):
            cmp = compare(left, right)
            if cmp < 0:
                sum += idx
            idx += 1
        print(sum)
        