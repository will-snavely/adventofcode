from aoc2019.intcode import IntCodeProcess

test_inputs = [
    "inputs/day19"
]


def scan(icp, x, y):
    child = icp.fork()
    child.send(x, y)
    child.simulate()
    return child.flush()[0]


def part1(path):
    controller = IntCodeProcess.compile(path)
    counter = 0
    for y in range(50):
        line = ""
        for x in range(50):
            if scan(controller, x, y) == 1:
                counter += 1
                line += "#"
            else:
                line += "."
    return counter


def part2(path):
    parent = IntCodeProcess.compile(path)
    seen = {}

    def lookup(a, b):
        if (a, b) not in seen:
            seen[(a, b)] = scan(parent, a, b)
        return seen[(a, b)]

    def scan_line(b, offset=0):
        a = offset
        state = 0
        beam_start = None
        beam_end = None

        while a > 0:
            s = lookup(a, b)
            if s == 1:
                a -= 1
            else:
                break

        while state != 2:
            s = lookup(a, b)
            if state == 0:
                if s == 1:
                    beam_start = a
                    state = 1
            elif state == 1:
                if s == 0:
                    beam_end = a
                    state = 2
            a += 1
        return beam_start, beam_end

    def square_fits(a, b):
        corners = [
            lookup(a, b),
            lookup(a + 99, b),
            lookup(a, b + 99),
            lookup(a + 99, b + 99)
        ]
        return all(c == 1 for c in corners)

    left = 0
    right = 1000
    while left < right:
        mid = (right + left) // 2
        start, end = scan_line(mid, (mid * 3) // 5)
        fits = any(square_fits(off, mid) for off in range(start, end))
        if mid == left:
            break
        elif fits:
            right = mid
        else:
            left = mid

    line = left
    for cur_line in range(line - 10, line + 10):
        start, end = scan_line(cur_line, (cur_line * 3) // 5)
        for off in range(start, end):
            if square_fits(off, cur_line):
                return off, cur_line, off * 10000 + cur_line


def process(path):
    with open(path) as f:
        print(part1(path))
        print(part2(path))


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
