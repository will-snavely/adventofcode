test_inputs = [
    "inputs/day3"
]


def wire_positions(wire):
    x = 0
    y = 0
    result = list()
    for op in wire:
        amt = int(op[1:])
        if op[0] == "R":
            for dx in range(1, amt + 1):
                result.append((x + dx, y))
            x += amt
        elif op[0] == "L":
            for dx in range(1, amt + 1):
                result.append((x - dx, y))
            x -= amt
        elif op[0] == "U":
            for dy in range(1, amt + 1):
                result.append((x, y + dy))
            y += amt
        elif op[0] == "D":
            for dy in range(1, amt + 1):
                result.append((x, y - dy))
            y -= amt
    return result


def process(path):
    print("Input:", path)
    with open(path) as f:
        lines = f.readlines()
        idx = 0
        while idx < len(lines):
            wire1 = lines[idx].strip().split(",")
            wire2 = lines[idx + 1].strip().split(",")

            wire1_pos = wire_positions(wire1)
            wire2_pos = wire_positions(wire2)
            intersections = set(wire1_pos) & set(wire2_pos)
            print("\tPart 1:", min([abs(x) + abs(y) for x, y in intersections]))

            steps = [
                wire1_pos.index(isect) + wire2_pos.index(isect) + 2
                for isect in intersections
            ]
            print("\tPart 2:", min(steps))
            idx += 2


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
