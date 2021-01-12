test_inputs = [
    "inputs/day8"
]

import collections



def parse_layers(xs, width, height):
    layers = []
    index = 0
    while index < len(xs):
        layers.append(xs[index: index + (width * height)])
        index += width * height
    return layers


def combine(layers):
    result = []
    for px in zip(*layers):
        pixel_value = 2
        for p in px:
            if p in [0, 1]:
                pixel_value = p
                break
        result.append(pixel_value)
    return result


def render(image, width, height, replace):
    index = 0
    for _ in range(height):
        print("".join([replace[c] for c in image[index: index + width]]))
        index += width


def process(path):
    print("Input:", path)
    with open(path) as f:
        for line in f:
            raw = [int(c) for c in line]
            layers = parse_layers(raw, 25, 6)
            counts = []
            for layer in layers:
                counter = collections.Counter(layer)
                counts.append((counter[0], counter[1], counter[2]))
            target = min(counts)
            print("\tPart 1:", target[1] * target[2])
            image = combine(layers)
            render(image, 25, 6, {1: "#", 0: " "})


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
