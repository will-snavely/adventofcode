test_inputs = [
    "inputs/day17_test1"
]

from aoc2019.intcode import IntCodeProcess

deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
opposite = {0: 2, 1: 3, 2: 0, 3: 1}


def parse_image(output):
    result = []
    row = []
    for x in output:
        value = chr(x)
        if value == "\n":
            if row:
                result.append(row)
                row = []
            else:
                break
        else:
            row.append(value)
    return result


def draw(image, path=None):
    path_points = set()
    if path is not None:
        path_points = set([p[1] for p in path])
    for row in range(len(image)):
        line = []
        for col in range(len(image[row])):
            if (row, col) in path_points:
                line.append("P")
            else:
                line.append(image[row][col])
        print("".join(line))


def adj(image, point, kind=None):
    result = []
    for dir, delta in enumerate(deltas):
        p = (point[0] + delta[0], point[1] + delta[1])
        if 0 <= p[0] < len(image) and 0 <= p[1] < len(image[p[0]]):
            if kind is None or image[p[0]][p[1]] == kind:
                result.append((dir, p))
    return result


def find(image, c):
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] == c:
                return row, col
    return None


def turn(dir1, dir2):
    diff = (dir2 - dir1) % 4
    if diff == 3:
        return "R"
    elif diff == 1:
        return "L"


def pathfind(img, pos):
    path = []
    commands = []
    facing = 2
    while True:
        options = [m for m in adj(img, pos, "#") if m[0] != opposite[facing]]
        if not options:
            break
        directions = [o[0] for o in options]
        if facing in directions:
            pos = (pos[0] + deltas[facing][0], pos[1] + deltas[facing][1])
            path.append((facing, pos))
            commands[-1] += 1
        else:
            commands.append(turn(facing, directions[0]))
            commands.append(0)
            facing = directions[0]

    return path, commands


def part1(path):
    icp = IntCodeProcess.compile(path)
    icp.simulate()
    output = icp.flush()
    image = parse_image(output)
    calibration = 0
    for row in range(len(image)):
        for col in range(len(image[row])):
            if image[row][col] == "#":
                if all(image[i][j] == "#" for _, (i, j) in adj(image, (row, col))):
                    calibration += row * col
    print(calibration)


def generate_encodings(
        encodings,
        sentence,
        index,
        depth,
        sequence,
        results):
    if index == len(sentence):
        results.append((encodings.copy(), sequence))
        return

    for size in range(2, 11):
        if index + size > len(sentence):
            break
        word = tuple(sentence[index:index + size])
        if word in encodings:
            generate_encodings(
                encodings,
                sentence,
                index + size,
                depth,
                sequence + [encodings[word]],
                results)
        else:
            if len(encodings) < 3:
                encodings[word] = depth
                generate_encodings(
                    encodings,
                    sentence,
                    index + size,
                    depth + 1,
                    sequence + [depth],
                    results)
                del encodings[word]


def part2(path):
    icp = IntCodeProcess.compile(path)
    icp.memory[0] = 2
    icp.simulate()
    output = icp.flush()
    image = parse_image(output)

    path, commands = pathfind(image, find(image, "^"))

    symbols = []
    for index in range(0, len(commands), 2):
        symbols.append((commands[index], commands[index + 1]))

    alphabet = set(symbols)
    letter_to_int = {}
    int_to_letter_str = {}
    for idx, letter in enumerate(alphabet):
        letter_to_int[letter] = idx
        int_to_letter_str[idx] = "{},{}".format(letter[0], letter[1])

    letter_size = {}
    for i, s in int_to_letter_str.items():
        letter_size[i] = len(s)

    sentence = [letter_to_int[symbol] for symbol in symbols]
    results = list()
    generate_encodings({}, sentence, 0, 0, [], results)
    suitable_encodings = []
    for encoding, sequence in results:
        suitable = True
        for transform in encoding:
            program_length = sum([letter_size[x] for x in transform]) + len(transform) - 1
            if program_length > 20:
                suitable = False
                break
        if suitable:
            suitable_encodings.append((encoding, sequence))

    labels = {0: "A", 1: "B", 2: "C"}
    if suitable_encodings:
        encoding, sequence = suitable_encodings[0]
    else:
        print("No suitable encodings found.")
        return

    programs = {}
    programs["main"] = ",".join([labels[elem] for elem in sequence])
    for seq, eid in encoding.items():
        programs[labels[eid]] = ",".join([int_to_letter_str[i] for i in seq])

    for prog in ["main", "A", "B", "C"]:
        print("Sending {}:".format(prog), programs[prog])
        for c in programs[prog]:
            icp.send(ord(c))
        icp.send(ord("\n"))
        icp.simulate()

    icp.send(ord("n"))
    icp.send(ord("\n"))
    icp.simulate()
    print(icp.flush()[-1])


def process(path):
    with open(path) as f:
        part1(path)
        part2(path)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
