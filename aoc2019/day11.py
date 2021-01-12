import collections

test_inputs = [
    "inputs/day11"
]

from aoc2019.intcode import IntCodeProcess


def paint(program, starting_color=None):
    proc = IntCodeProcess(program)
    robot_x = 0
    robot_y = 0
    robot_direction = 0
    painted_panels = collections.defaultdict(list)
    if starting_color:
        painted_panels[(0, 0)].append(starting_color)
    while proc.state != "done":
        pos = (robot_x, robot_y)
        color = 0
        if pos in painted_panels:
            color = painted_panels[pos][-1]

        proc_input = color
        proc.send(proc_input)
        proc.run()
        outputs = proc.flush()
        if len(outputs) == 2:
            new_color = outputs[0]
            turn = outputs[1]
            painted_panels[pos].append(new_color)
            if turn == 1:
                robot_direction = (robot_direction + 1) % 4
            else:
                robot_direction = (robot_direction - 1) % 4
            if robot_direction == 0:
                robot_y += 1
            elif robot_direction == 1:
                robot_x += 1
            elif robot_direction == 2:
                robot_y -= 1
            elif robot_direction == 3:
                robot_x -= 1
    return painted_panels


def process(path):
    print("Input:", path)
    with open(path) as f:
        program = [int(x) for x in f.readline().strip().split(",")]
        print(len(paint(program)))

        events = paint(program, starting_color=1)
        white_panels = [e for e in events if events[e][-1] == 1]
        xs = [p[0] for p in white_panels]
        ys = [p[1] for p in white_panels]
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        rows = []
        for y in range(min_y, max_y + 1):
            row = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in white_panels:
                    row += "#"
                else:
                    row += " "
            rows.append(row)
        for row in reversed(rows):
            print(row)


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
