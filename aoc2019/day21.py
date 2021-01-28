from aoc2019.intcode import IntCodeProcess

test_inputs = [
    "inputs/day21"
]


def encode(data):
    return [ord(c) for c in data]


def decode_single(char):
    try:
        return chr(char)
    except:
        return "int({})".format(char)


def decode(data):
    return "".join([decode_single(c) for c in data])


def run_script(intcode_path, script_path):
    with open(script_path) as f:
        script = f.readlines()
    controller = IntCodeProcess.compile(intcode_path)
    controller.simulate()
    print(decode(controller.flush()))
    for line in script:
        line = line.strip()
        if line:
            controller.send(*encode(line + "\n"))
    controller.simulate()
    print(decode(controller.flush()))


def process(path):
    run_script(path, "inputs/day21_script_part1")
    run_script(path, "inputs/day21_script_part2")


def main():
    for path in test_inputs:
        process(path)


if __name__ == "__main__":
    main()
