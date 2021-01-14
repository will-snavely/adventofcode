import collections

test_inputs = [
    "inputs/day16"
]


def phase(signal, base_pattern):
    result = []
    for i in range(len(signal)):
        print(i)
        offset = 0
        count = i + 1
        limit = i + 1
        transformed = 0
        for elem in signal[i:]:
            if count == limit:
                offset = (offset + 1) % len(base_pattern)
                count = 0
            transformed += base_pattern[offset] * elem
            count += 1
        result.append(abs(transformed) % 10)
    return result


def part1(signal):
    for _ in range(100):
        signal = phase(signal, [0, 1, 0, -1])
    print("".join([str(i) for i in signal[:8]]))


def sums(signal):
    sums = collections.defaultdict(int)
    sums[0] = signal[0]
    for idx in range(1, len(signal)):
        sums[idx] = signal[idx] + sums[idx - 1]
    return sums


def phase2(signal, offset, sum_map):
    output_size = len(signal)
    result = [0] * len(signal)
    for i in range(offset, output_size):
        step = i + 1
        j = i
        out = 0
        counter = 0
        while j < output_size:
            index = counter % 4
            k = min(j + step - 1, output_size - 1)
            m = j - 1
            if index == 0:
                left_sum = sum_map[k]
                right_sum = sum_map[m]
                out += left_sum - right_sum
            elif index == 2:
                left_sum = sum_map[k]
                right_sum = sum_map[m]
                out -= left_sum - right_sum
            j += step
            counter += 1
        result[i] = abs(out) % 10
    return result


def part2(signal):
    message_offset = int("".join([str(i) for i in signal[:7]]))
    print(message_offset)
    print(len(signal))
    signal = signal * 10000
    for i in range(100):
        sum_map = sums(signal)
        signal = phase2(signal, message_offset, sum_map)
    print("".join([str(i) for i in signal[message_offset:message_offset + 8]]))


def process(path):
    with open(path) as f:
        for line in f:
            signal = [int(d) for d in line.strip()]
            part2(signal)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
