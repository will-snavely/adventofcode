import re

test_inputs = [
    "inputs/day10"
]

line_re = (
    r"position=<\s*([0-9\-]+)\s*,\s*([0-9\-]+).*>\s*"
    r"velocity=<\s*([0-9\-]+)\s*,\s*([0-9\-]+).*>.*"
)
line_pattern = re.compile(line_re)


class Particle:
    def __init__(self, pos, velocity):
        self.pos = pos
        self.velocity = velocity

    def update(self, dir=1):
        self.pos = (
            self.pos[0] + self.velocity[0] * dir,
            self.pos[1] + self.velocity[1] * dir
        )


def draw(particles):
    points = set(p.pos for p in particles)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in points:
                row += "#"
            else:
                row += "."
        print(row)


def explore(cur, points, visited):
    visited.add(cur)
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            neighbor = (cur[0] + dx, cur[1] + dy)
            if neighbor in points and neighbor not in visited:
                explore(neighbor, points, visited)


def connected_components(particles):
    remaining = set(p.pos for p in particles)
    result = []
    for p in particles:
        if p.pos in remaining:
            seen = set()
            explore(p.pos, remaining, seen)
            remaining = remaining - seen
            result.append(remaining)
    return result


def process(path):
    with open(path) as f:
        particles = []
        for line in f:
            match = line_pattern.match(line)
            if match:
                vals = [int(m) for m in match.groups()]
                particles.append(Particle(tuple(vals[:2]), tuple(vals[2:])))

    counter = 0
    for p in particles:
        p.update(10000)
    while True:
        components = connected_components(particles)
        if len(components) < 10:
            draw(particles)
            print(counter + 10000)
            break

        for p in particles:
            p.update()
        counter += 1


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
